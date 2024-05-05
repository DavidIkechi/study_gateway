from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class DisciplineModel(Base):
    __tablename__ = "discipline_model"
    id = Column(Integer, primary_key=True, index=True)
    discipline_name = Column(String(100), unique=True, nullable=False)
    icons = Column(TEXT, nullable=True)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    #define the static methods
    @staticmethod
    def get_discipline_object(db: Session):
        return db.query(DisciplineModel)
    
    # get discipline by ID
    @staticmethod
    def get_discipline_by_id(db: Session, id: int):
        return DisciplineModel.get_discipline_object(db).get(id)
    
    # get discipline by slug
    @staticmethod
    def get_discipline_by_slug(db:Session, slug: str):
        return DisciplineModel.get_discipline_object(db).filter_by(slug=slug).first()
    
    # get all disciplines
    @staticmethod
    def get_all_disciplines(db: Session):
        return DisciplineModel.get_discipline_object(db)
    
    