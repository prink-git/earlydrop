from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import supabase

app = FastAPI(title="EarlyDrop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ActionPayload(BaseModel):
    action: str
    note: str | None = ""

@app.get("/")
def home():
    return {"message": "EarlyDrop backend is running 🚀"}

@app.get("/students")
def get_students():
    students = supabase.table("students") \
        .select("id, full_name, course") \
        .limit(50).execute().data

    risks = supabase.table("risk_scores") \
        .select("student_id, risk_score").execute().data

    risk_map = {}
    for r in risks:
        if r["student_id"] not in risk_map:
            risk_map[r["student_id"]] = r["risk_score"]

    result = []
    for s in students:
        score = risk_map.get(s["id"], 0)
        level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
        result.append({
            "id": s["id"],
            "name": s["full_name"],
            "course": s["course"],
            "risk_score": score,
            "risk_level": level
        })
    return result


@app.get("/students/{student_id}/timeline")
def student_timeline(student_id: str):
    features = supabase.table("weekly_features") \
        .select("week, avg_session_time, videos_completed") \
        .eq("student_id", student_id) \
        .order("week").execute().data

    risks = supabase.table("risk_scores") \
        .select("week, risk_score") \
        .eq("student_id", student_id) \
        .order("week").execute().data

    interventions = supabase.table("interventions") \
        .select("action, created_at") \
        .eq("student_id", student_id) \
        .order("created_at", desc=True).execute().data

    return {
        "engagement": features,
        "risk": risks,
        "interventions": interventions
    }


@app.post("/students/{student_id}/action")
def take_action(student_id: str, payload: ActionPayload):
    supabase.table("interventions").insert({
        "student_id": student_id,
        "action": payload.action,
        "note": payload.note or ""
    }).execute()

    return {"status": "ok"}
