# Base Model Module
# This module defines the base SQLAlchemy model class that other models inherit from

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Create the base class for declarative models
Base = declarative_base()

class BaseModel(Base):
    """Base model class that provides common fields and functionality for all models
    
    This abstract base class defines common columns that should be present in all database tables:
    - id: Primary key for unique record identification
    - created_at: Timestamp for when the record was created
    - updated_at: Timestamp that automatically updates when the record is modified
    
    All other models should inherit from this class to maintain consistent table structure.
    """
    __abstract__ = True
    
    # Primary key for all tables
    id = Column(Integer, primary_key=True, index=True)
    
    # Automatic timestamp fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())