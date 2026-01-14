from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import joblib
from supabase import create_client
from sklearn.ensemble import IsolationForest

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase env vars not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    data = supabase.table("weekly_features").select("*").execute().data
    df = pd.DataFrame(data)

    X = df[[
        "avg_session_time",
        "videos_completed",
        "quizzes_attempted",
        "days_active",
        "gap_variance"
    ]]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42
    )
    model.fit(X)

    joblib.dump(model, "anomaly_model.pkl")
    print("✅ Model trained & saved")

if __name__ == "__main__":
    main()
