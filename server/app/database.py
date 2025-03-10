# Database configuration and session management
# This file sets up SQLAlchemy engine, session factory, and database connection handling

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create SQLAlchemy engine instance using the configured database URL
engine = create_engine(settings.DATABASE_URL)

# Create session factory with autocommit and autoflush disabled for better control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to manage database sessions
# This ensures proper session handling and cleanup for each request
def get_db():
    db = SessionLocal()
    try:
        yield db  # Use as a context manager to handle session lifecycle
    finally:
        db.close()  # Ensure session is closed even if an error occurs