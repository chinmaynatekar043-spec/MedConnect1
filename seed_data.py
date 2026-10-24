from db import get_db

PROVIDERS = [
    {
        "name": "Aarogya Care Desk",
        "is_available": 1,
        "provider_type": "Medical Contact",
        "specialty": "General Health Guidance",
        "phone": "+91 90000 10001",
        "email": "care1@example.test",
        "address": "Demo Road, Palghar",
        "city": "Palghar",
        "state": "Maharashtra",
        "latitude": 19.6967,
        "longitude": 72.7699,
        "emergency": 0,
        "experience_years": 6,
        "qualification": "Registered Nurse - Demo Profile",
        "availability": "09:00 AM - 08:00 PM",
        "notes": "For general guidance and referral only. Demo contact."
    },
    {
        "name": "Swasthya First Response",
        "is_available": 1,
        "provider_type": "Medical Contact",
        "specialty": "First Aid Guidance",
        "phone": "+91 90000 10002",
        "email": "firstaid@example.test",
        "address": "Station Area, Saphale",
        "city": "Saphale",
        "state": "Maharashtra",
        "latitude": 19.5787,
        "longitude": 72.8215,
        "emergency": 0,
        "experience_years": 5,
        "qualification": "Registered Nurse - Demo Profile",
        "availability": "08:00 AM - 10:00 PM",
        "notes": "Minor first-aid guidance and escalation advice. Demo contact."
    },
    {
        "name": "Dr. Meera Shah",
        "is_available": 1,
        "provider_type": "Doctor",
        "specialty": "General Medicine",
        "phone": "+91 90000 20001",
        "email": "meera.shah@example.test",
        "address": "Demo Clinic, Palghar West",
        "city": "Palghar",
        "state": "Maharashtra",
        "latitude": 19.7005,
        "longitude": 72.7650,
        "emergency": 0,
        "experience_years": 11,
        "qualification": "MBBS, MD General Medicine - Demo Profile",
        "availability": "10:00 AM - 07:00 PM",
        "notes": "General physician. Demo profile only."
    },
    {
        "name": "Dr. Rohan Kulkarni",
        "is_available": 0,
        "provider_type": "Doctor",
        "specialty": "Pediatrics",
        "phone": "+91 90000 20002",
        "email": "rohan.k@example.test",
        "address": "Demo Children's Clinic, Palghar",
        "city": "Palghar",
        "state": "Maharashtra",
        "latitude": 19.7050,
        "longitude": 72.7760,
        "emergency": 0,
        "experience_years": 9,
        "qualification": "MBBS, MD Pediatrics - Demo Profile",
        "availability": "11:00 AM - 08:00 PM",
        "notes": "Pediatric consultation. Demo profile only."
    },
    {
        "name": "Dr. Sana Khan",
        "is_available": 1,
        "provider_type": "Doctor",
        "specialty": "Dermatology",
        "phone": "+91 90000 20003",
        "email": "sana.khan@example.test",
        "address": "Demo Skin Clinic, Boisar",
        "city": "Boisar",
        "state": "Maharashtra",
        "latitude": 19.8037,
        "longitude": 72.7558,
        "emergency": 0,
        "experience_years": 8,
        "qualification": "MBBS, MD Dermatology - Demo Profile",
        "availability": "09:30 AM - 06:30 PM",
        "notes": "Skin and allergy consultation. Demo profile only."
    },
    {
        "name": "Dr. Arjun Patil",
        "is_available": 0,
        "provider_type": "Doctor",
        "specialty": "Orthopedics",
        "phone": "+91 90000 20004",
        "email": "arjun.patil@example.test",
        "address": "Demo Ortho Centre, Virar",
        "city": "Virar",
        "state": "Maharashtra",
        "latitude": 19.4564,
        "longitude": 72.7925,
        "emergency": 0,
        "experience_years": 13,
        "qualification": "MBBS, MS Orthopedics - Demo Profile",
        "availability": "10:00 AM - 05:00 PM",
        "notes": "Bone, joint and injury consultation. Demo profile only."
    },
    {
        "name": "Dr. Nikhil Deshmukh",
        "is_available": 1,
        "provider_type": "Doctor",
        "specialty": "Cardiology",
        "phone": "+91 90000 20005",
        "email": "nikhil.d@example.test",
        "address": "Demo Heart Clinic, Vasai",
        "city": "Vasai",
        "state": "Maharashtra",
        "latitude": 19.3919,
        "longitude": 72.8397,
        "emergency": 1,
        "experience_years": 16,
        "qualification": "MBBS, MD, DM Cardiology - Demo Profile",
        "availability": "On-call + OPD",
        "notes": "Cardiology specialist. Demo profile only."
    },
    {
        "name": "Dr. Isha Menon",
        "is_available": 1,
        "provider_type": "Doctor",
        "specialty": "Neurology",
        "phone": "+91 90000 20006",
        "email": "isha.menon@example.test",
        "address": "Demo Neuro Centre, Thane",
        "city": "Thane",
        "state": "Maharashtra",
        "latitude": 19.2183,
        "longitude": 72.9781,
        "emergency": 1,
        "experience_years": 14,
        "qualification": "MBBS, MD, DM Neurology - Demo Profile",
        "availability": "10:00 AM - 06:00 PM",
        "notes": "Neurology specialist. Demo profile only."
    },
    {
        "name": "Palghar MultiCare Hospital",
        "is_available": 1,
        "provider_type": "Hospital",
        "specialty": "Multi-Specialty",
        "phone": "+91 90000 30001",
        "email": "palghar.hospital@example.test",
        "address": "Demo Hospital Road, Palghar",
        "city": "Palghar",
        "state": "Maharashtra",
        "latitude": 19.6930,
        "longitude": 72.7740,
        "emergency": 1,
        "experience_years": 20,
        "qualification": "Multi-specialty Hospital - Demo Profile",
        "availability": "24 x 7",
        "notes": "Emergency and multi-specialty care. Demo hospital."
    },
    {
        "name": "Boisar Emergency & Trauma Centre",
        "is_available": 1,
        "provider_type": "Hospital",
        "specialty": "Emergency Medicine",
        "phone": "+91 90000 30002",
        "email": "boisar.emergency@example.test",
        "address": "Demo MIDC Road, Boisar",
        "city": "Boisar",
        "state": "Maharashtra",
        "latitude": 19.8012,
        "longitude": 72.7572,
        "emergency": 1,
        "experience_years": 18,
        "qualification": "Emergency Hospital - Demo Profile",
        "availability": "24 x 7",
        "notes": "Emergency and trauma services. Demo hospital."
    },
    {
        "name": "Vasai Critical Care Hospital",
        "is_available": 1,
        "provider_type": "Hospital",
        "specialty": "Critical Care",
        "phone": "+91 90000 30003",
        "email": "vasai.critical@example.test",
        "address": "Demo Medical Campus, Vasai",
        "city": "Vasai",
        "state": "Maharashtra",
        "latitude": 19.3960,
        "longitude": 72.8410,
        "emergency": 1,
        "experience_years": 22,
        "qualification": "Critical Care Hospital - Demo Profile",
        "availability": "24 x 7",
        "notes": "ICU and emergency services. Demo hospital."
    }
]

CONDITIONS = [
    ("cold", "minor", "General Medicine", "cold runny nose sneezing mild cough"),
    ("fever", "minor", "General Medicine", "fever mild temperature weakness"),
    ("headache", "minor", "General Medicine", "headache mild migraine"),
    ("skin rash", "minor", "Dermatology", "rash itching skin allergy"),
    ("minor cut", "minor", "General Health Guidance", "cut scratch small wound first aid"),
    ("stomach pain", "minor", "General Medicine", "stomach pain digestion acidity nausea"),
    ("child fever", "minor", "Pediatrics", "child kid baby fever cough"),
    ("joint pain", "minor", "Orthopedics", "joint knee shoulder bone pain"),
    ("chest pain", "major", "Cardiology", "chest pain pressure heart breathing"),
    ("severe bleeding", "major", "Emergency Medicine", "heavy bleeding severe wound blood"),
    ("unconscious", "major", "Emergency Medicine", "unconscious faint not responding"),
    ("stroke signs", "major", "Neurology", "stroke face droop weakness speech"),
    ("severe breathing problem", "major", "Emergency Medicine", "breathing difficulty breathless choking"),
    ("major accident", "major", "Emergency Medicine", "accident trauma fracture crash"),
    ("seizure", "major", "Neurology", "seizure fit convulsion"),
    ("heart emergency", "major", "Cardiology", "heart attack severe chest pain cardiac")
]


def seed():
    conn = get_db()
    cur = conn.cursor()

    provider_count = cur.execute("SELECT COUNT(*) FROM providers").fetchone()[0]
    if provider_count == 0:
        cur.executemany(
            """
            INSERT INTO providers (
                name, provider_type, specialty, phone, email, address, city, state,
                latitude, longitude, emergency, is_available, experience_years, qualification,
                availability, notes
            )
            VALUES (
                :name, :provider_type, :specialty, :phone, :email, :address, :city, :state,
                :latitude, :longitude, :emergency, :is_available, :experience_years, :qualification,
                :availability, :notes
            )
            """,
            PROVIDERS
        )

    condition_count = cur.execute("SELECT COUNT(*) FROM conditions").fetchone()[0]
    if condition_count == 0:
        cur.executemany(
            "INSERT INTO conditions(name, severity, recommended_specialty, keywords) VALUES (?, ?, ?, ?)",
            CONDITIONS
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed()
    print("Demo data inserted.")
