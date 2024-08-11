from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class SemesterModel(Base):
    __tablename__ = "semesters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))

    @staticmethod
    def create_semester(semester_data: dict):
        return SemesterModel(**semester_data)

    @staticmethod
    def get_semester_by_id(db: Session, semester_id: int):
        return db.query(SemesterModel).filter_by(id=semester_id).first()
    
    @staticmethod
    def get_semester_by_slug(db: Session, slug: str):
        return db.query(SemesterModel).filter_by(slug=slug).first()

    @staticmethod
    def get_all_semesters(db: Session):
        return db.query(SemesterModel).all()
    
    @staticmethod
    def update_semester(db: Session, semester_id: int, semester_data: dict):
        semester = SemesterModel.get_semester_by_id(db, semester_id)
        for key, value in semester_data.items():
            setattr(semester, key, value)
        return semester