from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class DegreeTypeModel(Base):
    __tablename__ = "degree_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    descriptions = relationship("UniversityDescription", back_populates="deg_types")

    @staticmethod
    def create_degree_type(degree_data: dict):
        return DegreeTypeModel(**degree_data)

    @staticmethod
    def get_degree_type_by_id(db: Session, degree_id: int):
        return db.query(DegreeTypeModel).filter_by(id=degree_id).first()
    
    @staticmethod
    def get_degree_type_by_slug(db: Session, slug: str):
        return db.query(DegreeTypeModel).filter_by(slug=slug).first()

    @staticmethod
    def get_all_degree_types(db: Session):
        return db.query(DegreeTypeModel).all()
    
    @staticmethod
    def update_degree_type(db: Session, degree_id: int, degree_data: dict):
        degree_type = DegreeTypeModel.get_degree_type_by_id(db, degree_id)
        for key, value in degree_data.items():
            setattr(degree_type, key, value)
        return degree_type
