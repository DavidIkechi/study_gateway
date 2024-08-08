from .session import Base

from sqlalchemy import (
    Column, Enum, Integer, String, Boolean,
    BigInteger, TIMESTAMP, ForeignKey, Float,
    JSON, TEXT, LargeBinary, DateTime, Date
)
import uuid
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import func

class MentorStudent(Base):
    __tablename__ = "ment_studs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    degree_id = Column(Integer, ForeignKey("degree_model.id"))
    course_id = Column(Integer, ForeignKey("course_model.id"))
    university_id = Column(Integer, ForeignKey('universities.id'))
    application_ref = Column(String(50), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    connected = Column(Boolean, default=True)
    completed = Column(Boolean, default=False)
    status = Column(Enum("pending", "accepted", "rejected", name="status_enum"), default="pending")
    # New fields for year and progress
    # year = Column(Integer, nullable=True)  # Use Date to store the year
    document_progress = Column(Float, default=0.0, nullable=False)  # Progress between 0 and 1
    admission_progress = Column(Float, default=0.0, nullable=False)  # Progress between 0 and 1
    visa_progress = Column(Float, default=0.0, nullable=False)  # Progress between 0 and 1
    created_at = Column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    degrees = relationship("DegreeModel", back_populates="ment_studs")
    courses = relationship("CourseModel", back_populates="ment_studs")
    university = relationship("UniversityModel", back_populates="ment_studs")
    user = relationship("UserModel", foreign_keys=[user_id], back_populates="mentee_relationships")
    mentor = relationship("UserModel", foreign_keys=[mentor_id], back_populates="mentor_relationships")


    @staticmethod
    def get_ment_studs_object(db: Session):
        return db.query(MentorStudent)

    @staticmethod
    def create_ment_studs(ment_studs_data: dict):
        ment_stud = MentorStudent(**ment_studs_data)
        return ment_stud

    @staticmethod
    def get_ment_studs_by_id(db: Session, id):
        return MentorStudent.get_ment_studs_object(db).get(id)

    @staticmethod
    def get_ment_studs_by_user_id(db: Session, user_id):
        return (
            MentorStudent.get_ment_studs_object(db)
            .filter_by(user_id=user_id)
            .first()
        )

    @staticmethod
    def update_ment_studs(db: Session, ment_studs_id, user_data: dict):
        ment_stud = MentorStudent.get_ment_studs_by_id(db, ment_studs_id)
        if ment_stud is None:
            return None
        for key, value in user_data.items():
            setattr(ment_stud, key, value)
        return ment_stud
