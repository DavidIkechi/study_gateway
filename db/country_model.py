from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class CountryModel(Base):
    __tablename__ = "country_model"
    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)

    cities = relationship('CityModel', back_populates="countries")
    states = relationship('StateModel', back_populates="countries")
    user_profiles = relationship('ProfileModel', back_populates="countries")
    
    #define the static methods
    @staticmethod
    def get_country_object(db: Session):
        return db.query(CountryModel)
    
    # get country by ID
    @staticmethod
    def get_country_by_id(db: Session, id: int):
        return CountryModel.get_country_object(db).get(id)
    
    # get country by slug
    @staticmethod
    def get_country_by_slug(db:Session, slug: str):
        return CountryModel.get_country_object(db).filter_by(slug=slug).first()

    # get country by name
    @staticmethod
    def get_country_by_name(db:Session, name: str):
        return CountryModel.get_country_object(db).filter_by(country_name=name).first()
    
    # get all countrys
    @staticmethod
    def get_all_countries(db: Session):
        return CountryModel.get_country_object(db)
    
    