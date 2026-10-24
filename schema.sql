
CREATE TABLE providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    provider_type TEXT NOT NULL,
    specialty TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    emergency INTEGER NOT NULL DEFAULT 0,
    is_available INTEGER NOT NULL DEFAULT 1,
    experience_years INTEGER DEFAULT 0,
    qualification TEXT,
    availability TEXT,
    notes TEXT
);

CREATE TABLE conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    severity TEXT NOT NULL,
    recommended_specialty TEXT NOT NULL,
    keywords TEXT NOT NULL
);

CREATE TABLE search_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    selected_severity TEXT,
    detected_severity TEXT,
    latitude REAL,
    longitude REAL,
    results_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
