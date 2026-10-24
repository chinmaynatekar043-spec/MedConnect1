
# MedConnect - Mini Project Report

## 1. Title
**MedConnect: Distance-Based Medical Help & Healthcare Contact Dashboard**

## 2. Problem Statement
When a patient experiences a health problem, they may not know whether they should contact a nearby medical professional, specialist, or hospital. The project provides one dashboard where the patient enters the problem and receives a ranked list of relevant nearby healthcare contacts.

## 3. Objective
- Provide a single patient-facing dashboard.
- Separate minor and major/serious cases.
- Suggest the type of provider to contact.
- Rank contacts based on geographic distance.
- Match problems to relevant specialties.
- Store healthcare providers and search history in a DBMS.
- Demonstrate Python data structures and algorithms.
- Provide simple analytics for searches and provider data.

## 4. Technology
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **DBMS:** SQLite
- **Data Structures:** List, Dictionary, Set, Heap
- **Algorithm:** Haversine distance + weighted provider ranking

## 5. Main Modules

### Patient Dashboard
Takes:
- health problem
- minor/major/auto severity
- provider type
- specialty
- radius
- latitude and longitude

### Severity Routing
A simple rule-based academic classifier looks for keywords associated with a major or minor problem.

This is not medical diagnosis. Its only purpose is to route the demo search.

### Distance Engine
Distance between patient and provider is calculated using the Haversine formula from latitude and longitude.

### Provider Ranking
Each provider receives a score based on:
- relevant specialty
- text match
- provider type
- emergency capability
- distance

### Database
SQLite contains:
- providers
- conditions
- search_logs

### Analytics
The project displays:
- total searches
- minor/major searches
- provider-type counts
- popular search terms
- recent database records

## 6. Data Structures

### List
Stores provider result records while processing.

### Dictionary
Stores enriched provider information, severity counts, and provider counts.

### Set
Used for token matching between user-entered problems and provider metadata.

### Heap
`heapq.nsmallest()` is used for efficient top-k ranking.

## 7. Haversine Formula
The Haversine formula estimates distance between two latitude/longitude points on Earth:

`d = 2R × asin(sqrt(a))`

where Earth radius `R = 6371 km`.

## 8. Database Relationships

```text
conditions
  └── provides lookup information for a search

search_logs
  └── stores each patient dashboard search

providers
  └── stores all doctors, hospitals and medical contacts
```

For this prototype the tables are intentionally loosely coupled, because providers can serve many conditions and a condition can match many providers.

## 9. Program Flow

```text
Patient opens dashboard
        |
        v
Enters problem + severity + location
        |
        v
Python checks problem keywords
        |
        v
Minor -------------------------- Major
  |                               |
Medical contacts/doctors     Doctors/hospitals
  |                               |
  +--------------+----------------+
                 |
                 v
        Read providers from SQLite
                 |
                 v
       Calculate distance in Python
                 |
                 v
       Calculate relevance score
                 |
                 v
          Heap-based ranking
                 |
                 v
        Show nearest results
                 |
                 v
          Save search log
```

## 10. Example
Input:
- Problem: `mild fever and cough`
- Severity: Auto
- Location: Palghar demo coordinates

Output:
- General Medicine providers and nearby medical contacts are prioritized.

Input:
- Problem: `severe chest pain and difficulty breathing`
- Severity: Auto

Output:
- Emergency-capable hospitals and relevant major-care doctors are prioritized.

## 11. Limitations
- Demo data is fictional.
- Keyword routing is not a medical diagnostic system.
- It does not verify professional credentials.
- It does not check live availability.
- It does not prescribe medicines.
- Geographic ranking depends on coordinates.

## 12. Future Scope
- Verified doctor and hospital accounts
- Appointment booking
- Real maps and directions
- Live hospital bed availability
- Login and patient profiles
- Secure consultation requests
- MongoDB deployment option
- Admin CRUD portal
- Real healthcare provider APIs
- Notifications and OTP


## 13. Availability Status
Each provider record contains an `is_available` field.

- `1` = Available
- `0` = Currently unavailable

Available doctors and medical contacts are slightly prioritized in ranking. Search cards and provider profiles show a green/red status indicator.
