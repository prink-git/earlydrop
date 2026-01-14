import os
import random
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase env vars not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

students = supabase.table("students").select("id").execute().data
random.shuffle(students)

n = len(students)

high = students[: int(0.2 * n)]
medium = students[int(0.2 * n): int(0.45 * n)]
low = students[int(0.45 * n):]

def update(student_ids, profile):
    for s in student_ids:
        supabase.table("weekly_features") \
            .update(profile) \
            .eq("student_id", s["id"]) \
            .execute()

update(high, {
    "avg_session_time": 4,
    "videos_completed": 0,
    "quizzes_attempted": 0,
    "days_active": 1,
    "gap_variance": 9
})

update(medium, {
    "avg_session_time": 15,
    "videos_completed": 2,
    "quizzes_attempted": 1,
    "days_active": 3,
    "gap_variance": 4
})

update(low, {
    "avg_session_time": 35,
    "videos_completed": 6,
    "quizzes_attempted": 3,
    "days_active": 5,
    "gap_variance": 1
})

print("🔥 Injected realistic behavior diversity")
