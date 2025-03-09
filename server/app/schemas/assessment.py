from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class AssessmentBase(BaseModel):
    candidate_id: int
    resume_file_path: Optional[str] = None

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentResponse(AssessmentBase):
    id: int
    status: str
    responses: Dict[str, str] = {}
    result: Optional[Dict[str, Any]] = None
    resume_file_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class ResponseSubmit(BaseModel):
    question_id: int
    response_text: str

class AssessmentResult(BaseModel):
    big_five: Dict[str, float]  # Scores for each Big Five trait
    mbti: str  # MBTI personality type
    strengths: List[str]
    weaknesses: List[str]
    career_recommendations: List[str]