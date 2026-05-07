"""
Pydantic models for request/response validation and data serialization.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StudentBase(BaseModel):
    """Base student model."""
    id: str
    name: str
    course: str
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: str

class StudentResponse(StudentBase):
    """Response model for student data."""
    pass

class RiskData(BaseModel):
    """Model for risk score data."""
    student_id: str
    risk_score: float = Field(..., ge=0, le=100)

class EngagementData(BaseModel):
    """Model for weekly engagement data."""
    week: int = Field(..., ge=1)
    avg_session_time: float = Field(..., ge=0)
    videos_completed: Optional[int] = None

class InterventionData(BaseModel):
    """Model for intervention records."""
    action: str
    created_at: datetime
    note: Optional[str] = None

class TimelineResponse(BaseModel):
    """Response model for student timeline."""
    engagement: List[EngagementData]
    risk: List[RiskData]
    interventions: List[InterventionData]

class ActionPayload(BaseModel):
    """Request model for taking an action."""
    action: str = Field(..., min_length=1, max_length=255)
    note: Optional[str] = Field(None, max_length=1000)

class ActionResponse(BaseModel):
    """Response model for action confirmation."""
    status: str
    message: Optional[str] = None
