from dotenv import load_dotenv
load_dotenv()

import os
import random
from datetime import datetime, timedelta
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase env vars not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

EVENT_TYPES = ["login", "video_watch", "quiz_attempt"]

def main():
    start = datetime.now() - timedelta(weeks=8)

    for i in range(300):
        student = supabase.table("students").insert({
            "name": f"Student_{i}",
            "email": f"student{i}@example.com"
        }).execute().data[0]

        events = []
        for week in range(8):
            for _ in range(random.randint(5, 12)):
                events.append({
                    "student_id": student["id"],
                    "event_type": random.choice(EVENT_TYPES),
                    "duration": random.randint(5, 60),
                    "created_at": (
                        start + timedelta(days=week*7 + random.randint(0,6))
                    ).isoformat()
                })

        supabase.table("events").insert(events).execute()

    print("✅ Fake real-world data generated")

if __name__ == "__main__":
    main()
