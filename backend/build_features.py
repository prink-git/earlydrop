import pandas as pd
from supabase import create_client

SUPABASE_URL = "https://lqzvxxhwpirjowkqwjys.supabase.co"
SUPABASE_KEY = "sb_secret_G2P7kak0XO54kQcrAqvBgA_1FwmxgZ2"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    events = supabase.table("events").select("*").execute().data
    df = pd.DataFrame(events)

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["week"] = df["created_at"].dt.isocalendar().week

    feature_rows = []

    for (student_id, week), g in df.groupby(["student_id", "week"]):
        feature_rows.append({
            "student_id": student_id,
            "week": int(week),
            "avg_session_time": g["duration"].mean(),
            "videos_completed": (g["event_type"] == "video_watch").sum(),
            "quizzes_attempted": (g["event_type"] == "quiz_attempt").sum(),
            "days_active": g["created_at"].dt.date.nunique(),
            "gap_variance": g["created_at"].sort_values().diff().dt.days.var()
        })

    features_df = pd.DataFrame(feature_rows).fillna(0)

    supabase.table("weekly_features").insert(
        features_df.to_dict(orient="records")
    ).execute()

    print("✅ Weekly features generated")

if __name__ == "__main__":
    main()
