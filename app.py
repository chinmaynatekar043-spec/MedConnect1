from flask import Flask, render_template, request, jsonify, abort
from db import init_db, get_db
from seed_data import seed
from search_engine import detect_severity, rank_providers

app = Flask(__name__)

DEFAULT_LAT = 19.6967
DEFAULT_LON = 72.7699


def setup_database():
    init_db()
    seed()


setup_database()


def find_condition(problem):
    problem = (problem or "").strip().lower()
    if not problem:
        return None

    conn = get_db()
    rows = conn.execute("SELECT * FROM conditions").fetchall()
    conn.close()

    best = None
    best_score = 0

    query_tokens = set(problem.split())
    for row in rows:
        keywords = set((row["keywords"] or "").lower().split())
        name_tokens = set(row["name"].lower().split())
        overlap = len(query_tokens & (keywords | name_tokens))
        direct = 4 if row["name"].lower() in problem else 0
        score = overlap + direct

        if score > best_score:
            best = row
            best_score = score

    return best if best_score > 0 else None


@app.route("/")
def index():
    conn = get_db()
    provider_count = conn.execute("SELECT COUNT(*) FROM providers").fetchone()[0]
    hospital_count = conn.execute(
        "SELECT COUNT(*) FROM providers WHERE provider_type='Hospital'"
    ).fetchone()[0]
    doctor_count = conn.execute(
        "SELECT COUNT(*) FROM providers WHERE provider_type='Doctor'"
    ).fetchone()[0]
    contact_count = conn.execute(
        "SELECT COUNT(*) FROM providers WHERE provider_type='Medical Contact'"
    ).fetchone()[0]

    specialties = [
        row[0] for row in conn.execute(
            "SELECT DISTINCT specialty FROM providers ORDER BY specialty"
        ).fetchall()
    ]
    conn.close()

    return render_template(
        "index.html",
        provider_count=provider_count,
        hospital_count=hospital_count,
        doctor_count=doctor_count,
        contact_count=contact_count,
        specialties=specialties,
        default_lat=DEFAULT_LAT,
        default_lon=DEFAULT_LON
    )


@app.route("/search")
def search():
    problem = request.args.get("problem", "").strip()
    severity_choice = request.args.get("severity", "auto").lower()
    provider_type = request.args.get("provider_type", "all")
    specialty_filter = request.args.get("specialty", "all")

    try:
        lat = float(request.args.get("lat", DEFAULT_LAT))
        lon = float(request.args.get("lon", DEFAULT_LON))
        radius = float(request.args.get("radius", 100))
    except ValueError:
        lat, lon, radius = DEFAULT_LAT, DEFAULT_LON, 100

    detected = detect_severity(problem)
    condition = find_condition(problem)

    if severity_choice in {"minor", "major"}:
        severity = severity_choice
    elif condition:
        severity = condition["severity"]
    else:
        severity = detected

    recommended_specialty = (
        condition["recommended_specialty"]
        if condition
        else ("Emergency Medicine" if severity == "major" else "General Medicine")
    )

    conn = get_db()
    query = "SELECT * FROM providers WHERE 1=1"
    params = []

    if provider_type != "all":
        query += " AND provider_type = ?"
        params.append(provider_type)

    if specialty_filter != "all":
        query += " AND specialty = ?"
        params.append(specialty_filter)

    # Sensible default filtering by severity.
    if provider_type == "all":
        if severity == "major":
            query += " AND provider_type IN ('Doctor', 'Hospital')"
        else:
            query += " AND provider_type IN ('Medical Contact', 'Doctor', 'Hospital')"

    providers = conn.execute(query, params).fetchall()

    ranked = rank_providers(
        providers,
        problem,
        severity,
        recommended_specialty,
        lat,
        lon,
        limit=50
    )

    ranked = [p for p in ranked if p["distance_km"] <= radius]

    conn.execute(
        """
        INSERT INTO search_logs (
            query, selected_severity, detected_severity,
            latitude, longitude, results_count
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            problem,
            severity_choice,
            severity,
            lat,
            lon,
            len(ranked)
        )
    )
    conn.commit()

    specialties = [
        row[0] for row in conn.execute(
            "SELECT DISTINCT specialty FROM providers ORDER BY specialty"
        ).fetchall()
    ]
    conn.close()

    return render_template(
        "results.html",
        results=ranked,
        problem=problem,
        severity=severity,
        detected=detected,
        condition=condition,
        recommended_specialty=recommended_specialty,
        lat=lat,
        lon=lon,
        radius=radius,
        provider_type=provider_type,
        specialty_filter=specialty_filter,
        specialties=specialties
    )


@app.route("/provider/<int:provider_id>")
def provider_detail(provider_id):
    conn = get_db()
    provider = conn.execute(
        "SELECT * FROM providers WHERE id = ?", (provider_id,)
    ).fetchone()
    conn.close()

    if not provider:
        abort(404)

    return render_template("provider.html", provider=provider)


@app.route("/analytics")
def analytics():
    conn = get_db()

    total_searches = conn.execute(
        "SELECT COUNT(*) FROM search_logs"
    ).fetchone()[0]

    severity_rows = conn.execute(
        """
        SELECT detected_severity, COUNT(*) AS total
        FROM search_logs
        GROUP BY detected_severity
        """
    ).fetchall()

    provider_rows = conn.execute(
        """
        SELECT provider_type, COUNT(*) AS total
        FROM providers
        GROUP BY provider_type
        ORDER BY total DESC
        """
    ).fetchall()

    popular_queries = conn.execute(
        """
        SELECT query, COUNT(*) AS total
        FROM search_logs
        WHERE TRIM(COALESCE(query, '')) <> ''
        GROUP BY LOWER(query)
        ORDER BY total DESC
        LIMIT 8
        """
    ).fetchall()

    recent_searches = conn.execute(
        """
        SELECT *
        FROM search_logs
        ORDER BY id DESC
        LIMIT 10
        """
    ).fetchall()

    conn.close()

    severity_counts = {row["detected_severity"]: row["total"] for row in severity_rows}
    provider_counts = {row["provider_type"]: row["total"] for row in provider_rows}

    return render_template(
        "analytics.html",
        total_searches=total_searches,
        severity_counts=severity_counts,
        provider_counts=provider_counts,
        popular_queries=popular_queries,
        recent_searches=recent_searches
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/providers")
def api_providers():
    problem = request.args.get("problem", "")
    severity = request.args.get("severity", "auto").lower()

    try:
        lat = float(request.args.get("lat", DEFAULT_LAT))
        lon = float(request.args.get("lon", DEFAULT_LON))
    except ValueError:
        lat, lon = DEFAULT_LAT, DEFAULT_LON

    if severity not in {"minor", "major"}:
        severity = detect_severity(problem)

    condition = find_condition(problem)
    recommended_specialty = (
        condition["recommended_specialty"]
        if condition
        else ("Emergency Medicine" if severity == "major" else "General Medicine")
    )

    conn = get_db()
    providers = conn.execute("SELECT * FROM providers").fetchall()
    conn.close()

    ranked = rank_providers(
        providers,
        problem,
        severity,
        recommended_specialty,
        lat,
        lon,
        limit=20
    )

    return jsonify({
        "problem": problem,
        "severity": severity,
        "recommended_specialty": recommended_specialty,
        "results": ranked
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
