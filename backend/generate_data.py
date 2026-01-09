import random
import uuid
from datetime import datetime, timedelta
from supabase import create_client

SUPABASE_URL = "https://lqzvxxhwpirjowkqwjys.supabase.co"
SUPABASE_KEY = "sb_secret_G2P7kak0XO54kQcrAqvBgA_1FwmxgZ2"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

EVENT_TYPES = ["login", "video_watch", "quiz_attempt"]

def generate_students(n=300):
    students = []
    for i in range(n):
        students.append({
            "name": f"Student_{i}",
            "email": f"student{i}@example.com"
        })
    return students

def generate_events(student_id, start_date):
    events = []
    active_level = random.uniform(0.6, 1.0)

    for week in range(8):
        weekly_events = int(active_level * random.randint(5, 12))

        for _ in range(weekly_events):
            event_type = random.choice(EVENT_TYPES)
            duration = random.randint(5, 60)

            events.append({
                "student_id": student_id,
                "event_type": event_type,
                "duration": duration,
                "created_at": (
                start_date + timedelta(days=week * 7 + random.randint(0, 6))
            ).isoformat()
})


        # silent disengagement
        active_level *= random.uniform(0.85, 1.0)

    return events

def main():
    start_date = datetime.now() - timedelta(weeks=8)

    students = generate_students()

    for s in students:
        student = supabase.table("students").insert(s).execute().data[0]
        events = generate_events(student["id"], start_date)

        if events:
            supabase.table("events").insert(events).execute()

    print("✅ Fake real-world data generated")

if __name__ == "__main__":
    main()
