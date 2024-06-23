from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class AdditionalUserDetails(Base):
    __tablename__ = 'additional_details'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    email_address2 = Column(String(100), nullable=True)
    address2 = Column(TEXT, nullable=True)
    course_extra = Column(String(255), nullable=True)
    highest_degree_extra = Column(String(255), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    users = relationship('UserModel', back_populates='user_details')
    
    @staticmethod
    def get_user_details_object(db: Session):
        return db.query(AdditionalUserDetails)
    
    @staticmethod
    def create_user_details(user_details_data:dict):
        return AdditionalUserDetails(**user_details_data)
    
    @staticmethod
    def get_user_details_by_id(db: Session, id):
        return AdditionalUserDetails.get_user_details_object(db).get(id)
 
    @staticmethod
    def get_user_details_by_user_id(db: Session, user_id):
        return AdditionalUserDetails.get_user_details_object(db).filter_by(user_id = user_id).first()
    
    @staticmethod
    def update_user_details(db: Session, user_details_id, user_data: dict):
        user = AdditionalUserDetails.get_user_details_by_id(db, user_details_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        return user
    