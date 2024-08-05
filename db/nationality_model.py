from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class NationalityModel(Base):
    __tablename__ = "nationality_model"
    id = Column(Integer, primary_key=True, index=True)
    nationality = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    user_profiles = relationship('ProfileModel', back_populates='nationalities')
    mentors = relationship('AdditionalMentors', back_populates='nationalities')


    
    #define the static methods
    @staticmethod
    def get_nationality_object(db: Session):
        return db.query(NationalityModel)
    
    # get nationality by ID
    @staticmethod
    def get_nationality_by_id(db: Session, id: int):
        return NationalityModel.get_nationality_object(db).get(id)
    
    # get nationality by slug
    @staticmethod
    def get_nationality_by_slug(db:Session, slug: str):
        return NationalityModel.get_nationality_object(db).filter_by(slug=slug).first()
    
    # get all nationalities
    @staticmethod
    def get_all_nationalities(db: Session):
        return NationalityModel.get_nationality_object(db)