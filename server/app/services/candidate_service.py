from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate
from typing import List, Optional

class CandidateService:
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