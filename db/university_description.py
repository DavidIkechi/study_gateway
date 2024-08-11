from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class UniversityDescription(Base):
    __tablename__ = "university_descriptions"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    state_id = Column(Integer, ForeignKey('state_universities.id', ondelete='CASCADE'), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id', ondelete='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('course_model.id', ondelete='CASCADE'), nullable=False)
    college_id = Column(Integer, ForeignKey('colleges_schools.id', ondelete='CASCADE'), nullable=False)
    description = Column(TEXT, nullable=True)
    degree_type = Column(Integer, ForeignKey('degree_types.id', ondelete='CASCADE'), nullable=False)
    tuition = Column(String(100), nullable=True)
    academic_level = Column(Enum("post graduate", "under graduate", name="level_enum"), default="under graduate")
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    state = relationship("StateUniversityModel", back_populates="descriptions")
    university = relationship("UniversityModel", back_populates="descriptions")
    courses = relationship("CourseModel", back_populates="descriptions")
    college = relationship("CollegeSchoolModel", back_populates="descriptions")
    deg_types = relationship("DegreeTypeModel", back_populates="descriptions")

    
    @staticmethod
    def create_university_description(description_data: dict):
        return UniversityDescription(**description_data)

    @staticmethod
    def get_description_by_id(db: Session, description_id: int):
        return db.query(UniversityDescription).filter_by(id=description_id).first()
    
    @staticmethod
    def get_description_by_slug(db: Session, slug: str):
        return db.query(UniversityDescription).filter_by(slug=slug).first()

    @staticmethod
    def get_descriptions_by_university_id(db: Session, university_id: int):
        return db.query(UniversityDescription).filter_by(university_id=university_id).all()

    @staticmethod
    def update_description(db: Session, description_id: int, description_data: dict):
        description = UniversityDescription.get_description_by_id(db, description_id)
        for key, value in description_data.items():
            setattr(description, key, value)
        return description