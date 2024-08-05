from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class AdditionalMentors(Base):
    __tablename__ = 'additional_mentors'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_extra = Column(String(255), nullable=True)
    highest_degree_extra = Column(String(255), nullable=True)
    nationality_id = Column(Integer, ForeignKey('nationality_model.id'))
    gender_id = Column(Integer, ForeignKey('gender_model.id'))
    language_id = Column(Integer, ForeignKey('language_model.id'))
    degree_id = Column(Integer, ForeignKey('degree_model.id'))
    course_id = Column(Integer, ForeignKey('course_model.id'))
    birth_date = Column(DateTime, nullable=True)

    address = Column(TEXT, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    users = relationship('UserModel', back_populates='mentors')
    nationalities = relationship('NationalityModel', back_populates='mentors')
    genders = relationship('GenderModel', back_populates='mentors')
    languages = relationship('LanguageModel', back_populates='mentors')
    degrees = relationship('DegreeModel', back_populates='mentors')
    courses = relationship('CourseModel', back_populates='mentors')

    @staticmethod
    def get_mentors_object(db: Session):
        return db.query(AdditionalMentors)
    
    @staticmethod
    def create_mentors(mentors_data:dict):
        return AdditionalMentors(**mentors_data)
    
    @staticmethod
    def get_mentors_by_id(db: Session, id):
        return AdditionalMentors.get_mentors_object(db).get(id)
 
    @staticmethod
    def get_mentors_by_user_id(db: Session, user_id):
        return AdditionalMentors.get_mentors_object(db).filter_by(user_id = user_id).first()
    
    @staticmethod
    def update_mentors(db: Session, mentors_id, user_data: dict):
        user = AdditionalMentors.get_mentors_by_id(db, mentors_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        return user
    