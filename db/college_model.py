from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class CollegeSchoolModel(Base):
    __tablename__ = "colleges_schools"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    university_id = Column(Integer, ForeignKey('universities.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    descriptions = relationship("UniversityDescription", back_populates="college")
        
    @staticmethod
    def create_college_school(college_data: dict):
        return CollegeSchoolModel(**college_data)

    @staticmethod
    def get_college_school_by_id(db: Session, college_id: int):
        return db.query(CollegeSchoolModel).filter_by(id=college_id).first()
    
    @staticmethod
    def get_college_school_by_slug(db: Session, slug: str):
        return db.query(CollegeSchoolModel).filter_by(slug=slug).first()

    @staticmethod
    def get_college_schools_by_university_id(db: Session, university_id: int):
        return db.query(CollegeSchoolModel).filter_by(university_id=university_id).all()
    
    @staticmethod
    def update_college_school(db: Session, college_id: int, college_data: dict):
        college_school = CollegeSchoolModel.get_college_school_by_id(db, college_id)
        for key, value in college_data.items():
            setattr(college_school, key, value)
        return college_school