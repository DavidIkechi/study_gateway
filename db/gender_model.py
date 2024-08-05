from .session import Base
from sqlalchemy import Column, Date, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
# from .base_table_model import BaseTable
sys.path.append("..")

class GenderModel(Base):
    __tablename__ = 'gender_model'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    user_profiles = relationship('ProfileModel', back_populates='genders')
    mentors = relationship('AdditionalMentors', back_populates='genders')


                        
    # define the static methods here.
    @staticmethod
    def create_gender_object(db: Session):
        return db.query(GenderModel)
    
    @staticmethod
    def check_gender_slug(db: Session, slug: str):
        return GenderModel.create_gender_object(db).filter_by(
            slug=slug).first()
        
    @staticmethod
    def create_gender(gender: dict):
        return GenderModel(**gender)

    @staticmethod
    def get_all_gender(db: Session):
        return GenderModel.create_gender_object(db)
        
    @staticmethod
    def get_gender_by_id(db: Session, gender_id: int):
        return GenderModel.create_gender_object(db).get(gender_id)
    
    @staticmethod
    def update_single_gender(db: Session, gender_id, gender_data):
        gender = GenderModel.get_gender_by_id(db, gender_id)
        for key, value in gender_data.items():
            setattr(gender, key, value)
        return gender