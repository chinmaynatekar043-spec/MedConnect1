from math import radians, sin, cos, asin, sqrt
import heapq
import re

EARTH_RADIUS_KM = 6371.0

MAJOR_KEYWORDS = {
    "chest pain", "heart attack", "severe bleeding", "heavy bleeding",
    "unconscious", "not responding", "stroke", "seizure", "convulsion",
    "difficulty breathing", "breathing difficulty", "choking",
    "major accident", "trauma", "severe burn", "poisoning"
}

MINOR_KEYWORDS = {
    "cold", "cough", "mild fever", "headache", "rash", "itching",
    "minor cut", "small wound", "acidity", "mild stomach pain",
    "joint pain", "sneezing"
}


def normalize(text):
    return re.sub(r"[^a-z0-9\s]", " ", (text or "").lower()).strip()


def detect_severity(problem):
    """Very simple rule-based demo classifier. Not a medical diagnosis."""
    text = normalize(problem)

    for keyword in MAJOR_KEYWORDS:
        if keyword in text:
            return "major"

    for keyword in MINOR_KEYWORDS:
        if keyword in text:
            return "minor"

    return "minor"


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def token_match_score(problem, specialty, name="", notes=""):
    tokens = set(normalize(problem).split())
    haystack = set(normalize(f"{specialty} {name} {notes}").split())
    if not tokens:
        return 0
    return len(tokens & haystack) / len(tokens)


def score_provider(provider, problem, severity, recommended_specialty, patient_lat, patient_lon):
    distance = haversine_km(
        patient_lat, patient_lon,
        provider["latitude"], provider["longitude"]
    )

    specialty_match = 1 if (
        recommended_specialty
        and (
            recommended_specialty.lower() in provider["specialty"].lower()
            or provider["specialty"].lower() in recommended_specialty.lower()
        )
    ) else 0

    text_match = token_match_score(
        problem,
        provider["specialty"],
        provider["name"],
        provider["notes"] or ""
    )

    type_bonus = 0
    if severity == "major":
        if provider["provider_type"] == "Hospital":
            type_bonus += 3.0
        elif provider["provider_type"] == "Doctor":
            type_bonus += 1.3
        if provider["emergency"]:
            type_bonus += 3.0
    else:
        if provider["provider_type"] == "Medical Contact":
            type_bonus += 2.0
        elif provider["provider_type"] == "Doctor":
            type_bonus += 1.5

    availability_bonus = 1.5 if provider.get("is_available", 1) else -2.0

    # Higher is better.
    score = (
        specialty_match * 4.0
        + text_match * 2.0
        + type_bonus
        + availability_bonus
        - min(distance, 100) * 0.035
    )

    return round(score, 3), round(distance, 2)


def rank_providers(providers, problem, severity, recommended_specialty, patient_lat, patient_lon, limit=20):
    enriched = []
    for row in providers:
        provider = dict(row)
        score, distance = score_provider(
            provider,
            problem,
            severity,
            recommended_specialty,
            patient_lat,
            patient_lon
        )
        provider["score"] = score
        provider["distance_km"] = distance
        enriched.append(provider)

    # Data-structure requirement: heap-based top-k ranking.
    # heapq.nsmallest is used on a tuple where negative score means higher score first.
    top = heapq.nsmallest(
        min(limit, len(enriched)),
        enriched,
        key=lambda p: (-p["score"], p["distance_km"], p["name"])
    )
    return top
