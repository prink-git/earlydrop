"""
This module defines the main API endpoints for the application.

Functions:
- home: Handles the home endpoint.
- health: Handles the health check endpoint.
- students: Retrieves student data.
- timeline: Retrieves the timeline for a specific student.
- take_action: Performs an action for a specific student.
"""

import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db import (
    get_students,
    get_risks,
    get_features,
    get_interventions,
    add_intervention
)
from models import (
    StudentResponse,
    TimelineResponse,
    ActionPayload,
    ActionResponse,
    EngagementData,
    RiskData,
    InterventionData
)
from exceptions import (
    EarlyDropException,
    DatabaseError,
    StudentNotFoundError,
    ValidationError
)

app = FastAPI(title="EarlyDrop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(EarlyDropException)
async def early_drop_exception_handler(request, exc: EarlyDropException):
    logger.error(f"EarlyDrop exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get("/", response_model=dict)
def home():
    """Health check and welcome message."""
    logger.info("Home endpoint accessed")
    try:
        return {"message": "EarlyDrop backend is running 🚀", "version": "1.0.0"}
    except Exception as e:
        logger.error(f"Error in home endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/health")
def health():
    logger.info("Health endpoint accessed")
    try:
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error in health endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_mock_students():
    """Load 500 mock students from CSV file for offline/fallback mode."""
    import csv
    from pathlib import Path
    
    csv_file = Path(__file__).parent / "data" / "students_500.csv"
    result = []
    
    # Load from CSV if available
    if csv_file.exists():
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                risk_scores = {}
                
                # Load risk scores to match with students
                risk_file = Path(__file__).parent / "data" / "risk_scores_500.csv"
                if risk_file.exists():
                    with open(risk_file, "r", encoding="utf-8") as rf:
                        risk_reader = csv.DictReader(rf)
                        for row in risk_reader:
                            risk_scores[row["student_id"]] = {
                                "risk_score": float(row.get("risk_score", 50)),
                                "risk_level": row.get("risk_level", "Medium")
                            }
                
                # Build student list
                for row in reader:
                    student_id = row["id"]
                    risk_data = risk_scores.get(student_id, {"risk_score": 50, "risk_level": "Medium"})
                    
                    result.append(StudentResponse(
                        id=student_id,
                        name=row.get("full_name", "Unknown"),
                        course=row.get("course", "Unknown"),
                        risk_score=risk_data["risk_score"],
                        risk_level=risk_data["risk_level"]
                    ))
            
            logger.info(f"Loaded {len(result)} mock students from CSV")
            return result
        except Exception as e:
            logger.warning(f"Failed to load CSV mock data: {e}")
    
    # Fallback to hard-coded minimal data if CSV not available
    return [
        StudentResponse(id="1", name="Alice Johnson", course="CS101", risk_score=75, risk_level="High"),
        StudentResponse(id="2", name="Bob Smith", course="CS101", risk_score=45, risk_level="Medium"),
        StudentResponse(id="3", name="Carol Davis", course="MATH201", risk_score=20, risk_level="Low"),
        StudentResponse(id="4", name="David Wilson", course="CS101", risk_score=85, risk_level="High"),
        StudentResponse(id="5", name="Eve Brown", course="PHYS301", risk_score=35, risk_level="Low"),
        StudentResponse(id="6", name="Frank Miller", course="MATH201", risk_score=60, risk_level="Medium"),
    ]


@app.get("/students", response_model=List[StudentResponse])
def students():
    """Retrieve all students with their current risk assessments."""
    logger.info("Students endpoint accessed")
    try:
        students_data = get_students()
        risks = get_risks()

        risk_map = {r["student_id"]: r["risk_score"] for r in risks}

        result = []
        for s in students_data:
            score = risk_map.get(s["id"], 0)
            level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"

            result.append(StudentResponse(
                id=s["id"],
                name=s["full_name"],
                course=s["course"],
                risk_score=score,
                risk_level=level
            ))

        return result
    except Exception as e:
        logger.warning(f"Supabase unavailable, serving mock data: {e}")
        return get_mock_students()


@app.get("/students/{student_id}/timeline", response_model=TimelineResponse)
def timeline(student_id: str):
    """Retrieve comprehensive timeline for a specific student."""
    logger.info(f"Timeline accessed for student_id: {student_id}")
    try:
        engagement = get_features(student_id)
        risks = get_risks()
        interventions = get_interventions(student_id)

        return TimelineResponse(
            engagement=engagement,
            risk=[r for r in risks if r["student_id"] == student_id],
            interventions=interventions
        )
    except Exception as e:
        logger.warning(f"Supabase unavailable for timeline, serving mock data: {e}")
        # Return mock timeline data
        mock_timeline = {
            "engagement": [
                {"week": 1, "avg_session_time": 45, "videos_completed": 8},
                {"week": 2, "avg_session_time": 38, "videos_completed": 6},
                {"week": 3, "avg_session_time": 25, "videos_completed": 3},
                {"week": 4, "avg_session_time": 15, "videos_completed": 1},
            ],
            "risk": [{"student_id": student_id, "risk_score": 75}],
            "interventions": [
                {"action": "Email sent", "created_at": "2026-05-05T10:00:00Z"},
                {"action": "Meeting scheduled", "created_at": "2026-05-04T14:30:00Z"},
            ]
        }
        return TimelineResponse(**mock_timeline)


@app.post("/students/{student_id}/action", response_model=ActionResponse)
def take_action(student_id: str, payload: ActionPayload):
    """Record an intervention action for a student."""
    logger.info(f"Action taken for student_id: {student_id} with payload: {payload}")
    try:
        add_intervention(student_id, payload.action, payload.note or "")
        return ActionResponse(
            status="ok",
            message=f"Intervention '{payload.action}' recorded for student {student_id}"
        )
    except Exception as e:
        logger.warning(f"Supabase unavailable, recording mock intervention: {e}")
        # Return mock success response
        return ActionResponse(
            status="ok",
            message=f"Intervention '{payload.action}' recorded for student {student_id} (mock mode)"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
