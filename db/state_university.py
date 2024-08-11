from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class StateUniversityModel(Base):
    __tablename__ = "state_universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))

    descriptions = relationship("UniversityDescription", back_populates="state")

    @staticmethod
    def create_state_university(state_university_data: dict):
        return StateUniversityModel(**state_university_data)

    @staticmethod
    def get_state_university_by_id(db: Session, state_university_id: int):
        return db.query(StateUniversityModel).filter_by(id=state_university_id).first()
    
    @staticmethod
    def get_state_university_by_slug(db: Session, slug: str):
        return db.query(StateUniversityModel).filter_by(slug=slug).first()

    @staticmethod
    def get_all_state_universities(db: Session):
        return db.query(StateUniversityModel).all()
    
    @staticmethod
    def update_state_university(db: Session, state_university_id: int, state_university_data: dict):
        state_university = StateUniversityModel.get_state_university_by_id(db, state_university_id)
        for key, value in state_university_data.items():
            setattr(state_university, key, value)
        return state_university
