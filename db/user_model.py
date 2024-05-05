from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(30), nullable=False)
    email_address = Column(String(20), nullable=False, unique=True)
    is_mentor = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_lock = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    is_setup = Column(Boolean, default=False)
    lock_count = Column(Integer, default=0)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    # define the static methods
    @staticmethod
    def get_user_object(db: Session):
        return db.query(UserModel)
    
    @staticmethod
    def create_user(user_data:dict):
        return UserModel(**user_data)
    
    @staticmethod
    def check_email(db: Session, email: str):
        return UserModel.get_user_object(db).filter_by(email_address = email).first()#
    
    @staticmethod
    def get_users(db: Session):
        return UserModel.get_user_object(db).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id):
        return UserModel.get_user_object(db).get(user_id)
    
    @staticmethod
    def update_user(db: Session, user_id, user_data: dict):
        user = UserModel.get_user_by_id(db, user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        return user
    
    