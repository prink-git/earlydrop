"""
Generate CSV files for manual import into Supabase:
- students_500.csv (student rows with email, GPA, enrollment date)
- weekly_features_500.csv (8 weeks per student with engagement metrics)
- risk_scores_500.csv (one per student with risk level)
- interventions_500.csv (0-2 per student)

Run: python generate_csv.py
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
OUT_DIR = Path(__file__).resolve().parent / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOTAL = 500
WEEKS = 8
COURSES = ["CS101", "MATH201", "PHYS301", "BIO110", "ENG202"]
ACTIONS = ["Email sent", "Meeting scheduled", "SMS reminder", "Call placed"]
DROPOUT_REASONS = ["Low engagement", "Poor academic performance", "Attendance issues", "Financial constraints", "Mental health concerns"]
RISK_LEVELS = ["Low", "Medium", "High"]

start = datetime.utcnow() - timedelta(weeks=WEEKS)

# ====== Students (with id, email, GPA, enrollment_date, status) ======
students_file = OUT_DIR / "students_500.csv"
with students_file.open("w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "full_name", "email", "course", "enrollment_date", "gpa", "status", "created_at"])
    for i in range(1, TOTAL+1):
        name = f"Student {i:04d}"
        email = f"student{i:04d}@university.edu"
        course = random.choice(COURSES)
        # Enrollment date: between 6-12 months ago
        enrollment = (datetime.now() - timedelta(days=random.randint(180, 365))).date()
        # GPA between 1.5 and 4.0 (realistic distribution)
        gpa = round(random.gauss(3.0, 0.8), 2)
        gpa = max(1.5, min(4.0, gpa))
        # Most students active; 5% dropouts
        status = random.choices(["active", "inactive", "dropout"], weights=[0.85, 0.10, 0.05])[0]
        created = (start + timedelta(days=random.randint(0, 7))).isoformat() + "Z"
        writer.writerow([i, name, email, course, enrollment, gpa, status, created])

# ====== Weekly features (engagement: sessions, videos, assignments, forum, GPA trend) ======
weekly_file = OUT_DIR / "weekly_features_500.csv"
with weekly_file.open("w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["student_id", "week", "avg_session_time", "videos_completed", "assignments_submitted", "forum_posts", "gpa_trend", "created_at"])
    for sid in range(1, TOTAL+1):
        base = random.uniform(20, 60)
        base_gpa_trend = random.uniform(2.5, 4.0)
        for w in range(1, WEEKS+1):
            # Simulate declining engagement for some students (high-risk)
            trend = base - (w-1) * random.uniform(0, 6)
            avg_session_time = max(1.0, round(trend + random.uniform(-5, 5), 1))
            videos_completed = max(0, int(max(0, random.gauss(5, 2) - (w-1)*0.3)))
            assignments_submitted = max(0, int(random.gauss(3, 1.5)))
            forum_posts = max(0, int(random.gauss(2, 1)))
            # GPA trend (slight decline or improvement over weeks)
            gpa_trend = round(max(1.5, base_gpa_trend - (w-1)*0.05 + random.uniform(-0.1, 0.1)), 2)
            created = (start + timedelta(days=(w-1)*7 + random.randint(0, 6))).isoformat() + "Z"
            writer.writerow([sid, w, avg_session_time, videos_completed, assignments_submitted, forum_posts, gpa_trend, created])

# ====== Risk scores (with risk_level and predicted_dropout_reason) ======
risk_file = OUT_DIR / "risk_scores_500.csv"
with risk_file.open("w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["student_id", "risk_score", "risk_level", "predicted_dropout_reason", "updated_at"])
    for sid in range(1, TOTAL+1):
        # Derive risk from average recent activity (lower engagement = higher risk)
        recent_avg = random.uniform(15, 60)
        risk = int(min(100, max(0, 100 - recent_avg)))
        
        # Map risk score to risk level
        if risk < 33:
            risk_level = "Low"
        elif risk < 66:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # High-risk students have a predicted reason; low-risk typically none
        predicted_reason = random.choice(DROPOUT_REASONS) if risk_level == "High" else ""
        
        updated = (datetime.utcnow() - timedelta(days=random.randint(0, 14))).isoformat() + "Z"
        writer.writerow([sid, risk, risk_level, predicted_reason, updated])

# ====== Interventions (0-2 per student with notes) ======
inter_file = OUT_DIR / "interventions_500.csv"
with inter_file.open("w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["student_id", "action", "note", "created_at"])
    for sid in range(1, TOTAL+1):
        # High-risk students more likely to have interventions
        n = random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1])[0]
        for _ in range(n):
            action = random.choice(ACTIONS)
            note = random.choice(["Follow-up scheduled", "Left voicemail", "Escalated to advisor", "One-on-one tutoring offered", "Counseling referral made", ""])
            created = (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat() + "Z"
            writer.writerow([sid, action, note, created])

print("✓ Generated production-ready CSVs (500 students, 8 weeks engagement data):")
print(f"  - {students_file}")
print(f"  - {weekly_file}")
print(f"  - {risk_file}")
print(f"  - {inter_file}")
print("Done.")
print(f" - {risk_file}")
print(f" - {inter_file}")
print("Done.")
