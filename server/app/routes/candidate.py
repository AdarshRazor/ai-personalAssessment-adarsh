# Candidate Management Routes
# This module handles candidate profile creation and retrieval operations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.candidate_service import CandidateService
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    candidate: CandidateCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new candidate profile
    
    Args:
        candidate: Candidate creation data
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        CandidateResponse: Created candidate profile
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        return CandidateService.create_candidate(db, candidate)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[CandidateResponse])
async def read_candidates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a paginated list of all candidates
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        List[CandidateResponse]: List of candidate profiles
    """
    candidates = CandidateService.get_candidates(db, skip=skip, limit=limit)
    return candidates

@router.get("/{candidate_id}", response_model=CandidateResponse)
async def read_candidate(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a specific candidate by ID
    
    Args:
        candidate_id: ID of the candidate to retrieve
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        CandidateResponse: Candidate profile if found
        
    Raises:
        HTTPException: If candidate not found
    """
    candidate = CandidateService.get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

@router.get("/email/{email}", response_model=CandidateResponse)
async def read_candidate_by_email(
    email: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a candidate by their email address
    
    Args:
        email: Email address to search for
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        CandidateResponse: Candidate profile if found
        
    Raises:
        HTTPException: If candidate not found
    """
    candidate = CandidateService.get_candidate_by_email(db, email)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate