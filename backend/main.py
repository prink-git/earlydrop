from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import (
    get_students,
    get_risks,
    get_features,
    get_interventions,
    add_intervention
)

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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/students")
def students():
    students = get_students()
    risks = get_risks()

    risk_map = {r["student_id"]: r["risk_score"] for r in risks}

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
def timeline(student_id: str):
    return {
        "engagement": get_features(student_id),
        "risk": [r for r in get_risks() if r["student_id"] == student_id],
        "interventions": get_interventions(student_id)
    }


@app.post("/students/{student_id}/action")
def take_action(student_id: str, payload: ActionPayload):
    add_intervention(student_id, payload.action, payload.note or "")
    return {"status": "ok"}
