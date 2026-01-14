from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import numpy as np
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase env vars not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def to_py(v):
    """Convert numpy / pandas types to pure Python"""
    if pd.isna(v):
        return 0
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    return v

def main():
    events = supabase.table("events").select("*").execute().data
    df = pd.DataFrame(events)

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["week"] = df["created_at"].dt.isocalendar().week

    rows = []

    for (student_id, week), g in df.groupby(["student_id", "week"]):
        row = {
            "student_id": student_id,
            "week": int(week),
            "avg_session_time": g["duration"].mean(),
            "videos_completed": (g["event_type"] == "video_watch").sum(),
            "quizzes_attempted": (g["event_type"] == "quiz_attempt").sum(),
            "days_active": g["created_at"].dt.date.nunique(),
            "gap_variance": g["created_at"]
                .sort_values()
                .diff()
                .dt.days
                .var(),
        }

        # 🔥 convert EVERYTHING to Python native
        clean_row = {k: to_py(v) for k, v in row.items()}
        rows.append(clean_row)

    supabase.table("weekly_features").insert(rows).execute()
    print("✅ Weekly features generated")

if __name__ == "__main__":
    main()
