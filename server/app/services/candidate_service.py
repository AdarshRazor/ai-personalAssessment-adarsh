# Candidate Service Module
# This module handles candidate profile management and data operations

from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate
from typing import List, Optional

class CandidateService:
    """Service class for managing candidate profiles
    
    This class provides methods for creating, retrieving, and updating
    candidate profiles in the system. It handles basic CRUD operations
    and ensures data consistency.
    
    The service maintains candidate information including:
    - Personal details (name, email)
    - Personality assessment results
    - Profile management
    
    All methods are implemented as static methods for stateless operation.
    """
    @staticmethod
    def create_candidate(db: Session, candidate: CandidateCreate) -> Candidate:
        # Check if candidate with same email already exists
        existing = db.query(Candidate).filter(Candidate.email == candidate.email).first()
        if existing:
            raise ValueError(f"Candidate with email {candidate.email} already exists")
        
        db_candidate = Candidate(
            name=candidate.name,
            email=candidate.email,
            personality_profile=None
        )
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        return db_candidate
    
    @staticmethod
    def get_candidate(db: Session, candidate_id: int) -> Optional[Candidate]:
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    @staticmethod
    def get_candidate_by_email(db: Session, email: str) -> Optional[Candidate]:
        return db.query(Candidate).filter(Candidate.email == email).first()
    
    @staticmethod
    def get_candidates(db: Session, skip: int = 0, limit: int = 100) -> List[Candidate]:
        return db.query(Candidate).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_candidate(db: Session, candidate_id: int, candidate: CandidateCreate) -> Optional[Candidate]:
        db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not db_candidate:
            return None
        
        for key, value in candidate.dict().items():
            setattr(db_candidate, key, value)
        
        db.commit()
        db.refresh(db_candidate)
        return db_candidate