from .session import Base
from sqlalchemy import Column, Enum, Numeric, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy.sql import text

import sys
sys.path.append("..")

class PricingModel(Base):
    __tablename__ = "pricing_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    price = Column(Numeric(precision=10, scale=2), default=Decimal("0.00"))
    requirement = Column(JSON, default=[])
    benefits = Column(JSON, default=[])
    description = Column(TEXT)
    package_id= Column(Integer, ForeignKey("package_model.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)

    packages = relationship('PackageModel', back_populates="pricing")
    
    #define the static methods
    @staticmethod
    def get_pricing_object(db: Session):
        return db.query(PricingModel)
    
    # get pricing by ID
    @staticmethod
    def get_pricing_by_id(db: Session, id: int):
        return PricingModel.get_pricing_object(db).get(id)
    
    # get pricing by slug
    @staticmethod
    def get_pricing_by_slug(db:Session, slug: str):
        return PricingModel.get_pricing_object(db).filter_by(slug=slug).first()
    
    @staticmethod
    def get_pricing_by_package(db: Session, package_id: int):
        return PricingModel.get_pricing_object(db).filter_by(package_id=package_id)
    # get all pricings
    @staticmethod
    def get_all_pricings(db: Session):
        return PricingModel.get_pricing_object(db)