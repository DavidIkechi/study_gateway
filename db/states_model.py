from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class StateModel(Base):
    __tablename__ = "state_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    country_id= Column(Integer, ForeignKey("country_model.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)

    countries = relationship('CountryModel', back_populates="states")
    user_profiles = relationship('ProfileModel', back_populates="states")

    #define the static methods
    @staticmethod
    def get_state_object(db: Session):
        return db.query(StateModel)
    
    # get state by ID
    @staticmethod
    def get_state_by_id(db: Session, id: int):
        return StateModel.get_state_object(db).get(id)
    
    # get state by slug
    @staticmethod
    def get_state_by_slug(db:Session, slug: str):
        return StateModel.get_state_object(db).filter_by(slug=slug).first()
    
    @staticmethod
    def get_state_by_country(db: Session, country_id: int):
        return StateModel.get_state_object(db).filter_by(country_id=country_id)
    # get all states
    @staticmethod
    def get_all_states(db: Session):
        return StateModel.get_state_object(db)