from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class SubscriberModel(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String(100), nullable=False, unique=True, index=True)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    # define the static methods
    @staticmethod
    def get_subscriber_object(db: Session):
        return db.query(SubscriberModel)
    
    @staticmethod
    def create_subscriber(subscriber_data:dict):
        return SubscriberModel(**subscriber_data)
    
    @staticmethod
    def check_email(db: Session, email: str):
        return SubscriberModel.get_subscriber_object(db).filter_by(email_address = email).first()#
    
    @staticmethod
    def get_subscribers(db: Session):
        return SubscriberModel.get_subscriber_object(db).all()