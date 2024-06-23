from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    email_address = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False, default="Doe")
    last_name = Column(String(255), nullable=False, default="Doe")
    is_mentor = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_lock = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    is_setup = Column(Boolean, default=False)
    lock_count = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)
    login_count = Column(BigInteger, default = 0)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    user_profiles = relationship('ProfileModel', back_populates='users')
    user_details = relationship('AdditionalUserDetails', back_populates='users')
    
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
    
    @staticmethod
    def get_user_by_email(db: Session, email:str):
        query = UserModel.get_user_object(db)
        query = query.with_entities(
            UserModel.id,
            UserModel.email_address,
            UserModel.is_verified,
            UserModel.is_setup
        )
        # filter out centers
        query = query.filter(UserModel.email_address == email)
        return query.first()