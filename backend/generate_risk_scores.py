import pandas as pd
import joblib
from supabase import create_client

SUPABASE_URL = "https://lqzvxxhwpirjowkqwjys.supabase.co"
SUPABASE_KEY = "sb_secret_G2P7kak0XO54kQcrAqvBgA_1FwmxgZ2"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    # 1️⃣ Load weekly features
    data = supabase.table("weekly_features").select("*").execute().data
    df = pd.DataFrame(data)

    # 2️⃣ Load trained model
    model = joblib.load("anomaly_model.pkl")

    # 3️⃣ Feature matrix
    X = df[
        [
            "avg_session_time",
            "videos_completed",
            "quizzes_attempted",
            "days_active",
            "gap_variance",
        ]
    ]

    # 4️⃣ Continuous anomaly score
    df["anomaly_score"] = model.decision_function(X)
    # lower score = more anomalous

    def compute_risk(score):
     if score < -0.08:
        return 85   # 🔴 High
     elif score < 0.03:
        return 55   # 🟡 Medium
     else:
        return 20   # 🟢 Low


    df["risk_score"] = df["anomaly_score"].apply(compute_risk)

    # 6️⃣ Explanation
    df["explanation"] = df.apply(explain, axis=1)

    records = df[
        ["student_id", "week", "risk_score", "explanation"]
    ].to_dict(orient="records")

    existing = supabase.table("risk_scores").select("id").execute().data
    if existing:
        supabase.table("risk_scores").delete().in_("id", [r["id"] for r in existing]).execute()

    supabase.table("risk_scores").insert(records).execute()

    print("✅ Risk scores regenerated with High / Medium / Low")


if __name__ == "__main__":
    main()
