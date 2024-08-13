from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class CollegeUniversityModel(Base):
    __tablename__ = "colleges_universities"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    college_id = Column(Integer, ForeignKey('colleges_schools.id'), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    description = Column(TEXT, nullable=True)
    
    college = relationship("CollegeSchoolModel", back_populates="college_universities")
    university = relationship("UniversityModel", back_populates="college_universities")

    @staticmethod
    def create_college_university(college_university_data: dict):
        return CollegeUniversityModel(**college_university_data)

    @staticmethod
    def get_college_university_by_id(db: Session, college_university_id: int):
        return db.query(CollegeUniversityModel).filter_by(id=college_university_id).first()

    @staticmethod
    def get_college_universities_by_university_id(db: Session, university_id: int):
        return db.query(CollegeUniversityModel).filter_by(university_id=university_id).all()
    
    @staticmethod
    def get_college_universities_by_college_id(db: Session, college_id: int):
        return db.query(CollegeUniversityModel).filter_by(college_id=college_id).all()

    @staticmethod
    def update_college_university(db: Session, college_university_id: int, college_university_data: dict):
        college_university = CollegeUniversityModel.get_college_university_by_id(db, college_university_id)
        for key, value in college_university_data.items():
            setattr(college_university, key, value)
        return college_university
