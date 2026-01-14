from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import joblib
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase env vars not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def compute_risk(score):
    if score < -0.08:
        return 85   # High
    elif score < 0.03:
        return 55   # Medium
    else:
        return 20   # Low


def explain(row):
    reasons = []
    if row["videos_completed"] <= 1:
        reasons.append("Very low video engagement")
    if row["quizzes_attempted"] == 0:
        reasons.append("No quiz participation")
    if row["days_active"] <= 2:
        reasons.append("Inactive on most days")
    if row["gap_variance"] >= 5:
        reasons.append("Irregular study pattern")
    return ", ".join(reasons) if reasons else "Healthy engagement pattern"


def main():
    data = supabase.table("weekly_features").select("*").execute().data
    df = pd.DataFrame(data)

    model = joblib.load("anomaly_model.pkl")

    X = df[
        [
            "avg_session_time",
            "videos_completed",
            "quizzes_attempted",
            "days_active",
            "gap_variance",
        ]
    ]

    anomaly_scores = model.decision_function(X)

    df["risk_score"] = [compute_risk(s) for s in anomaly_scores]
    df["explanation"] = df.apply(explain, axis=1)

    records = df[
        ["student_id", "week", "risk_score", "explanation"]
    ].to_dict(orient="records")

    # fetch IDs first
    existing = supabase.table("risk_scores").select("id").execute().data

    if existing:
        ids = [r["id"] for r in existing]
        supabase.table("risk_scores").delete().in_("id", ids).execute()

    
    supabase.table("risk_scores").insert(records).execute()

    print("✅ Risk scores generated")

if __name__ == "__main__":
    main()
