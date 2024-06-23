from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class CountryCodeModel(Base):
    __tablename__ = "country_code_model"
    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(100), unique=True, nullable=False)
    phone_code = Column(String(100), nullable=False)
    iso3 = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    #define the static methods
    @staticmethod
    def get_country_code_object(db: Session):
        return db.query(CountryCodeModel)
    
    # get country_code by ID
    @staticmethod
    def get_country_code_by_id(db: Session, id: int):
        return CountryCodeModel.get_country_code_object(db).get(id)
    
    # get country_code by slug
    @staticmethod
    def get_country_code_by_slug(db:Session, slug: str):
        return CountryCodeModel.get_country_code_object(db).filter_by(slug=slug).first()

    # get all country_codes
    @staticmethod
    def get_all_countries(db: Session):
        return CountryCodeModel.get_country_code_object(db)