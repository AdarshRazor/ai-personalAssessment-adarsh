from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

# Base schema for candidate data validation
class CandidateBase(BaseModel):
    """Base candidate model containing common attributes shared across candidate schemas.
    
    Attributes:
        name (str): Full name of the candidate
        email (EmailStr): Valid email address of the candidate, validated by Pydantic
    """
    name: str
    email: EmailStr

class CandidateCreate(CandidateBase):
    """Schema for creating a new candidate. Inherits all fields from CandidateBase."""
    pass

class CandidateResponse(CandidateBase):
    """Schema for returning candidate data in API responses.
    
    Extends CandidateBase with additional fields that represent candidate state and assessment results.
    
    Attributes:
        id (int): Unique identifier for the candidate
        personality_profile (Optional[Dict[str, Any]]): Results of personality assessment, if completed
        created_at (datetime): Timestamp when the candidate record was created
    """
    id: int
    personality_profile: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        orm_mode = True