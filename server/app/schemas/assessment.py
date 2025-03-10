from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

# Base schema for assessment data validation
class AssessmentBase(BaseModel):
    """Base assessment model containing common attributes shared across assessment schemas.
    
    Attributes:
        candidate_id (int): Foreign key reference to the candidate taking the assessment
        resume_file_path (Optional[str]): Path to the candidate's uploaded resume file, if any
    """
    candidate_id: int
    resume_file_path: Optional[str] = None

class AssessmentCreate(AssessmentBase):
    """Schema for creating a new assessment. Inherits all fields from AssessmentBase."""
    pass

class AssessmentResponse(AssessmentBase):
    """Schema for returning assessment data in API responses.
    
    Extends AssessmentBase with additional fields that are generated during assessment processing.
    
    Attributes:
        id (int): Unique identifier for the assessment
        status (str): Current status of the assessment (e.g., 'pending', 'completed')
        responses (Dict[str, str]): Dictionary mapping question IDs to candidate's responses
        result (Optional[Dict[str, Any]]): Assessment results after evaluation
        resume_file_path (Optional[str]): Path to the uploaded resume file
        created_at (datetime): Timestamp when the assessment was created
    """
    id: int
    status: str
    responses: Dict[str, str] = {}
    result: Optional[Dict[str, Any]] = None
    resume_file_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class ResponseSubmit(BaseModel):
    """Schema for submitting a response to a single assessment question.
    
    Attributes:
        question_id (int): ID of the question being answered
        response_text (str): Candidate's response to the question
    """
    question_id: int
    response_text: str

class AssessmentResult(BaseModel):
    """Schema for the final assessment results after evaluation.
    
    Attributes:
        big_five (Dict[str, float]): Numerical scores for each of the Big Five personality traits
        mbti (str): The determined Myers-Briggs Type Indicator personality type
        strengths (List[str]): List of identified candidate strengths
        weaknesses (List[str]): List of identified candidate weaknesses
        career_recommendations (List[str]): List of career paths that match the candidate's profile
    """
    big_five: Dict[str, float]  # Scores for each Big Five trait
    mbti: str  # MBTI personality type
    strengths: List[str]
    weaknesses: List[str]
    career_recommendations: List[str]