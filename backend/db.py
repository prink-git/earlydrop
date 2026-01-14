from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase env vars not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_students():
    return supabase.table("students") \
        .select("id, full_name, course") \
        .execute().data


def get_risks():
    return supabase.table("risk_scores") \
        .select("student_id, risk_score") \
        .execute().data


def get_features(student_id):
    return supabase.table("weekly_features") \
        .select("week, avg_session_time, videos_completed") \
        .eq("student_id", student_id) \
        .order("week") \
        .execute().data


def get_interventions(student_id):
    return supabase.table("interventions") \
        .select("action, created_at") \
        .eq("student_id", student_id) \
        .order("created_at", desc=True) \
        .execute().data


def add_intervention(student_id, action, note):
    supabase.table("interventions").insert({
        "student_id": student_id,
        "action": action,
        "note": note
    }).execute()
