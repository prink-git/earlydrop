# db.py
import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_supabase: Client | None = None

def get_supabase() -> Client | None:
    global _supabase
    if _supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("⚠️ Supabase env vars not set")
            return None
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase


# ---------- DATA ACCESS LAYER ----------

def get_students():
    sb = get_supabase()
    if not sb:
        return []
    return sb.table("students") \
        .select("id, full_name, course") \
        .limit(50) \
        .execute().data


def get_risks():
    sb = get_supabase()
    if not sb:
        return []
    return sb.table("risk_scores") \
        .select("student_id, risk_score") \
        .execute().data


def get_features(student_id):
    sb = get_supabase()
    if not sb:
        return []
    return sb.table("weekly_features") \
        .select("week, avg_session_time, videos_completed") \
        .eq("student_id", student_id) \
        .order("week") \
        .execute().data


def get_interventions(student_id):
    sb = get_supabase()
    if not sb:
        return []
    return sb.table("interventions") \
        .select("action, created_at") \
        .eq("student_id", student_id) \
        .order("created_at", desc=True) \
        .execute().data


def add_intervention(student_id, action, note):
    sb = get_supabase()
    if not sb:
        return
    sb.table("interventions").insert({
        "student_id": student_id,
        "action": action,
        "note": note
    }).execute()
