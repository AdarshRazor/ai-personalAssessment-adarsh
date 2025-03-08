from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.candidate_service import CandidateService

router = APIRouter()

@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    try:
        return CandidateService.create_candidate(db, candidate)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[CandidateResponse])
async def read_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    candidates = CandidateService.get_candidates(db, skip=skip, limit=limit)
    return candidates

@router.get("/{candidate_id}", response_model=CandidateResponse)
async def read_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = CandidateService.get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

@router.get("/email/{email}", response_model=CandidateResponse)
async def read_candidate_by_email(email: str, db: Session = Depends(get_db)):
    candidate = CandidateService.get_candidate_by_email(db, email)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate