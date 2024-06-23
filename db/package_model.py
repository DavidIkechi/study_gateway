from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class PackageModel(Base):
    __tablename__ = "package_model"
    id = Column(Integer, primary_key=True, index=True)
    package_name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)

    pricing = relationship('PricingModel', back_populates="packages")
    
    #define the static methods
    @staticmethod
    def get_package_object(db: Session):
        return db.query(PackageModel)
    
    # get package by ID
    @staticmethod
    def get_package_by_id(db: Session, id: int):
        return PackageModel.get_package_object(db).get(id)
    
    # get package by slug
    @staticmethod
    def get_package_by_slug(db:Session, slug: str):
        return PackageModel.get_package_object(db).filter_by(slug=slug).first()

    # get package by name
    @staticmethod
    def get_package_by_name(db:Session, name: str):
        return PackageModel.get_package_object(db).filter_by(package_name=name).first()
    
    # get all packages
    @staticmethod
    def get_all_packages(db: Session):
        return PackageModel.get_package_object(db)