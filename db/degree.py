from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class DegreeModel(Base):
    __tablename__ = "degree_model"
    id = Column(Integer, primary_key=True, index=True)
    degree_name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)

    user_profiles = relationship('ProfileModel', back_populates="degrees")
    mentors = relationship('AdditionalMentors', back_populates="degrees")
    ment_studs = relationship("MentorStudent", back_populates="degrees")


    #define the static methods
    @staticmethod
    def get_degree_object(db: Session):
        return db.query(DegreeModel)
    
    # get degree by ID
    @staticmethod
    def get_degree_by_id(db: Session, id: int):
        return DegreeModel.get_degree_object(db).get(id)
    
    # get degree by slug
    @staticmethod
    def get_degree_by_slug(db:Session, slug: str):
        return DegreeModel.get_degree_object(db).filter_by(slug=slug).first()

    # get degree by name
    @staticmethod
    def get_degree_by_name(db:Session, name: str):
        return DegreeModel.get_degree_object(db).filter_by(degree_name=name).first()
    
    # get all degrees
    @staticmethod
    def get_all_degrees(db: Session):
        return DegreeModel.get_degree_object(db)