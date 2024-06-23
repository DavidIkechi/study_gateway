from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class ProfileModel(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    gender_id = Column(Integer, ForeignKey('gender_model.id'))
    birth_date = Column(DateTime, nullable=True)
    address = Column(TEXT, nullable=True)
    nationality_id = Column(Integer, ForeignKey('nationality_model.id'))
    phone = Column(String(20), nullable=True)
    zip_code = Column(String(20), nullable=True)
    city = Column(String(20), nullable=True)
    country_id = Column(Integer, ForeignKey('country_model.id'))
    state_id = Column(Integer, ForeignKey('state_model.id'))
    degree_id = Column(Integer, ForeignKey('degree_model.id'))
    degree_sought_id = Column(Integer, ForeignKey('degree_sought.id'))
    course_id = Column(Integer, ForeignKey('course_model.id'))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    users = relationship('UserModel', back_populates='user_profiles')
    countries = relationship('CountryModel', back_populates='user_profiles')
    nationalities = relationship('NationalityModel', back_populates='user_profiles')
    genders = relationship('GenderModel', back_populates='user_profiles')
    states = relationship('StateModel', back_populates='user_profiles')
    degrees = relationship('DegreeModel', back_populates='user_profiles')
    degree_soughts = relationship('DegreeSoughtModel', back_populates='user_profiles')
    courses = relationship('CourseModel', back_populates='user_profiles')
    
    @staticmethod
    def get_profile_object(db: Session):
        return db.query(ProfileModel)
    
    @staticmethod
    def create_profile(profile_data:dict):
        return ProfileModel(**profile_data)
    
    @staticmethod
    def get_profile_by_id(db: Session, id):
        return ProfileModel.get_profile_object(db).get(id)
 
    @staticmethod
    def get_profile_by_user_id(db: Session, user_id):
        return ProfileModel.get_profile_object(db).filter_by(user_id = user_id).first()
    
    @staticmethod
    def update_profile(db: Session, user_profile_id, user_data: dict):
        user = ProfileModel.get_profile_by_id(db, user_profile_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        return user