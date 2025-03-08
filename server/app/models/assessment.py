from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Assessment(BaseModel):
    __tablename__ = "assessments"
    
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    status = Column(String, default="in_progress")  # in_progress, completed
    responses = Column(JSON, default={})  # Stores question_id: response pairs
    result = Column(JSON, nullable=True)  # Stores the assessment results
    
    candidate = relationship("Candidate", back_populates="assessments")

# Add relationship to Candidate model
from .candidate import Candidate
Candidate.assessments = relationship("Assessment", back_populates="candidate")