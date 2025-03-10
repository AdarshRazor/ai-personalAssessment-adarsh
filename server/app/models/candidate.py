# Candidate Model Module
# This module defines the Candidate model for storing applicant information

from sqlalchemy import Column, String, JSON
from .base import BaseModel

class Candidate(BaseModel):
    """Candidate model for managing job applicant profiles
    
    This model stores essential information about job candidates including their
    personal details and personality assessment results. It maintains a relationship
    with the Assessment model for tracking evaluation progress.
    
    Attributes:
        name (str): Full name of the candidate
        email (str): Unique email address for contact
        personality_profile (dict): JSON field storing the analyzed personality traits
        assessments (list): Relationship field containing associated Assessment instances
    """
    __tablename__ = "candidates"
    
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    personality_profile = Column(JSON, nullable=True)  # Stores the final personality profile