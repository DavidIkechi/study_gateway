from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class LanguageModel(Base):
    __tablename__ = "language_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    mentors = relationship('AdditionalMentors', back_populates='languages')

    
    #define the static methods
    @staticmethod
    def get_language_object(db: Session):
        return db.query(LanguageModel)
    
    # get language by ID
    @staticmethod
    def get_language_by_id(db: Session, id: int):
        return LanguageModel.get_language_object(db).get(id)
    
    # get language by slug
    @staticmethod
    def get_language_by_slug(db:Session, slug: str):
        return LanguageModel.get_language_object(db).filter_by(slug=slug).first()
    
    @staticmethod
    def get_all_languages(db: Session):
        return LanguageModel.get_language_object(db)