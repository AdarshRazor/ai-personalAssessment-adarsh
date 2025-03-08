from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import questions, assessments, candidates, auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(questions, prefix="/api/questions", tags=["questions"])
app.include_router(assessments, prefix="/api/assessments", tags=["assessments"])
app.include_router(candidates, prefix="/api/candidates", tags=["candidates"])
app.include_router(auth, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Personality Assessment System API"}