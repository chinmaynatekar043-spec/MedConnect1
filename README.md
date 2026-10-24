# MedConnect - Medical Help & Nearby Care Dashboard

A college-ready Python project that helps a patient find nearby medical contacts based on:
- problem/keyword
- minor vs major case
- specialty
- distance from patient
- emergency capability

## Technology Used
- Python
- Flask
- SQLite (DBMS)
- Data Structures: lists, dictionaries, heaps (`heapq`) for nearest-provider ranking
- HTML/CSS/JavaScript
- Haversine formula for geographic distance

## Important safety note
This demo does **not** diagnose illness or prescribe medicine. For minor problems it lists qualified medical contacts the patient can contact. For major/emergency problems it prioritizes doctors and hospitals.

All names, phone numbers, email addresses, and addresses in the seed data are fictional demo data.

## Features
1. Patient dashboard
2. Search by symptom/problem
3. Minor / Major / Auto severity selection
4. Automatic simple keyword-based severity suggestion
5. Find contacts by distance
6. Filter by provider type
7. Recommended specialty matching
8. Emergency-capable provider prioritization
9. Provider detail page
10. SQLite database with seeded data
11. Search history / analytics page
12. JSON API endpoint
13. Browser geolocation button
14. Responsive dashboard UI
15. Availability status for doctors / assigned medical contacts

## Project Structure

```text
medical_help_dashboard/
├── app.py
├── db.py
├── search_engine.py
├── seed_data.py
├── requirements.txt
├── medical_help.db          # created automatically
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── provider.html
│   ├── analytics.html
│   └── about.html
└── static/
    ├── style.css
    └── app.js
```

## Run

```bash
cd medical_help_dashboard
python -m venv .venv
```

### macOS/Linux
```bash
source .venv/bin/activate
```

### Windows
```powershell
.venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
python app.py
```

Open:
```text
http://127.0.0.1:5000
```

## Demo Location
The default demo latitude/longitude is near Palghar, Maharashtra:
- Latitude: 19.6967
- Longitude: 72.7699

You can click **Use my location** in the dashboard to use browser GPS/location permission.

## DBMS Tables

### providers
Stores doctors, hospitals and medical contacts.

### conditions
Stores demo health problems, severity and recommended specialty.

### search_logs
Stores search text, selected severity, coordinates and time.

## Data Structures Used
- `dict`: severity keyword lookup and provider grouping
- `list`: provider result records
- `heapq.nsmallest`: efficiently returns nearest / highest-ranked K providers
- `set`: unique specialties and matching tokens

## Distance Formula
The project uses the Haversine formula:

`distance = 2R * asin(sqrt(a))`

where `R = 6371 km`.

## Possible Future Improvements
- Login/signup
- Real doctor/hospital APIs
- Appointment booking
- OTP verification
- Admin dashboard
- MongoDB version
- Map integration
- Chat/video consultation
- Real-time hospital bed availability
- Verified medical professional accounts
