from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    email: EmailStr

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int
    personality_profile: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        orm_mode = True