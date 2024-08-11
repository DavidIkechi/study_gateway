from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class LocationModel(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey('universities.id', ondelete='CASCADE'), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_urls = Column(JSON, nullable=True)  # JSON field for storing image URLs
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))

    university = relationship("UniversityModel", back_populates="location")

    @staticmethod
    def create_location(location_data: dict):
        return LocationModel(**location_data)

    @staticmethod
    def get_location_by_id(db: Session, location_id: int):
        return db.query(LocationModel).filter_by(id=location_id).first()
    
    @staticmethod
    def get_location_by_slug(db: Session, slug: str):
        return db.query(LocationModel).filter_by(slug=slug).first()

    @staticmethod
    def get_location_by_university_id(db: Session, university_id: int):
        return db.query(LocationModel).filter_by(university_id=university_id).first()
    
    @staticmethod
    def update_location(db: Session, location_id: int, location_data: dict):
        location = LocationModel.get_location_by_id(db, location_id)
        for key, value in location_data.items():
            setattr(location, key, value)
        return location