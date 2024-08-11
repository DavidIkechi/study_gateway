from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class CourseModel(Base):
    __tablename__ = "course_model"
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)

    user_profiles = relationship('ProfileModel', back_populates="courses")
    mentors = relationship('AdditionalMentors', back_populates="courses")
    ment_studs = relationship("MentorStudent", back_populates="courses")
    descriptions = relationship("UniversityDescription", back_populates="courses")
    
    #define the static methods
    @staticmethod
    def get_course_object(db: Session):
        return db.query(CourseModel)
    
    # get course by ID
    @staticmethod
    def get_course_by_id(db: Session, id: int):
        return CourseModel.get_course_object(db).get(id)
    
    # get course by slug
    @staticmethod
    def get_course_by_slug(db:Session, slug: str):
        return CourseModel.get_course_object(db).filter_by(slug=slug).first()

    # get course by name
    @staticmethod
    def get_course_by_name(db:Session, name: str):
        return CourseModel.get_course_object(db).filter_by(course_name=name).first()
    
    # get all courses
    @staticmethod
    def get_all_courses(db: Session):
        return CourseModel.get_course_object(db)