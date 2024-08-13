from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class UniversityModel(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    locations = Column(String(255), nullable=True)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    url = Column(String(255))
    address = Column(TEXT, nullable=True)
    
    ment_studs = relationship("MentorStudent", back_populates="university")
    location = relationship("LocationModel", back_populates="university")
    descriptions = relationship("UniversityDescription", back_populates="university")
    college_universities = relationship("CollegeUniversityModel", back_populates="university")
    
    @staticmethod
    def get_university_object(db: Session):
        return db.query(UniversityModel)
    
    @staticmethod
    def create_university(university_data:dict):
        return UniversityModel(**university_data)
    
    @staticmethod
    def get_university_by_id(db: Session, id):
        return UniversityModel.get_university_object(db).get(id)
 
    @staticmethod
    def get_university_by_slug(db: Session, slug):
        return UniversityModel.get_university_object(db).filter_by(slug = slug).first()
    
    @staticmethod
    def update_university(db: Session, university_id, user_data: dict):
        user = UniversityModel.get_university_by_id(db, university_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        return user
    
    