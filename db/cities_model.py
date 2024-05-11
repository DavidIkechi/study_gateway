from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class CityModel(Base):
    __tablename__ = "city_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    country_id= Column(Integer, ForeignKey("country_model.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)

    countries = relationship('CountryModel', back_populates="cities")

    
    #define the static methods
    @staticmethod
    def get_city_object(db: Session):
        return db.query(CityModel)
    
    # get city by ID
    @staticmethod
    def get_city_by_id(db: Session, id: int):
        return CityModel.get_city_object(db).get(id)
    
    # get city by slug
    @staticmethod
    def get_city_by_slug(db:Session, slug: str):
        return CityModel.get_city_object(db).filter_by(slug=slug).first()
    
    @staticmethod
    def get_city_by_country(db: Session, country_id: int):
        return CityModel.get_city_object(db).filter_by(country_id=country_id)
    # get all citys
    @staticmethod
    def get_all_cities(db: Session):
        return CityModel.get_city_object(db)
    
    