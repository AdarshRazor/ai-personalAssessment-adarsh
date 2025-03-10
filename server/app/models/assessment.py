# Assessment Model Module
# This module defines the Assessment model for tracking candidate evaluations

from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Assessment(BaseModel):
    """Assessment model for managing candidate personality evaluations
    
    This model tracks the progress and results of personality assessments for candidates.
    It stores question responses, final results, and maintains a relationship with the
    candidate being assessed.
    
    Attributes:
        candidate_id (int): Foreign key linking to the candidate being assessed
        status (str): Current status of the assessment ('in_progress' or 'completed')
        responses (dict): JSON field storing question responses as {question_id: response_text}
        result (dict): JSON field storing the final assessment results and analysis
        resume_file_path (str): Path to the candidate's uploaded resume PDF
        candidate (Candidate): Relationship to the Candidate model
    """
    __tablename__ = "assessments"
    
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    status = Column(String, default="in_progress")  # in_progress, completed
    responses = Column(JSON, default={})  # Stores question_id: response pairs
    result = Column(JSON, nullable=True)  # Stores the assessment results
    resume_file_path = Column(String, nullable=True)  # Stores the path to the uploaded resume PDF
    
    # Bidirectional relationship with Candidate model
    candidate = relationship("Candidate", back_populates="assessments")

# Add relationship to Candidate model
from .candidate import Candidate
Candidate.assessments = relationship("Assessment", back_populates="candidate")