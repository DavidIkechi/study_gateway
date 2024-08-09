from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import and_, not_, or_
from fastapi_pagination.ext.sqlalchemy import paginate as pg
from fastapi_pagination import Params, paginate

import sys
sys.path.append("..")

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255), nullable=False)
    email_address = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False, default="Doe")
    last_name = Column(String(255), nullable=False, default="Doe")
    is_mentor = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_lock = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    photo = Column(LargeBinary, nullable=True)  # Add photo column

    is_setup = Column(Boolean, default=False)
    lock_count = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)
    login_count = Column(BigInteger, default = 0)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.now(), 
                        onupdate=datetime.now(), nullable=False)
    
    user_profiles = relationship('ProfileModel', back_populates='users')
    user_details = relationship('AdditionalUserDetails', back_populates='users')
    mentors = relationship('AdditionalMentors', back_populates='users')
    # Define relationships with the foreign_keys parameter
    mentee_relationships = relationship("MentorStudent", foreign_keys="[MentorStudent.user_id]", back_populates="user")
    mentor_relationships = relationship("MentorStudent", foreign_keys="[MentorStudent.mentor_id]", back_populates="mentor")
    
    # define the static methods
    @staticmethod
    def get_user_object(db: Session):
        return db.query(UserModel)
    
    @staticmethod
    def create_user(user_data:dict):
        return UserModel(**user_data)
    
    @staticmethod
    def check_email(db: Session, email: str):
        return UserModel.get_user_object(db).filter_by(email_address = email).first()#
    
    @staticmethod
    def get_users(db: Session):
        return UserModel.get_user_object(db).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id):
        return UserModel.get_user_object(db).get(user_id)
    
    @staticmethod
    def update_user(db: Session, user_id, user_data: dict):
        user = UserModel.get_user_by_id(db, user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email:str):
        query = UserModel.get_user_object(db)
        query = query.with_entities(
            UserModel.id,
            UserModel.email_address,
            UserModel.is_verified,
            UserModel.is_setup
        )
        # filter out centers
        query = query.filter(UserModel.email_address == email)
        return query.first()
    
    @staticmethod
    def get_mentors(db: Session, user_id: int, language_id: int = None, course_id: int = None, page: int = None, page_size: int = 10):
        from db.main_model import AdditionalMentors, MentorStudent, DegreeModel, CourseModel

        # Build the query
        query = db.query(UserModel).join(
            AdditionalMentors, AdditionalMentors.user_id == UserModel.id
        ).filter(
            UserModel.is_mentor == True,
            UserModel.is_setup == True
        )

        # Apply additional filters if provided
        if language_id:
            query = query.filter(AdditionalMentors.language_id == language_id)
        if course_id:
            query = query.filter(AdditionalMentors.course_id == course_id)

        # Build a list of mentors with additional information about the user-mentor relationship
        mentors_with_status = []
        for mentor in query.all():
            additional_mentor = db.query(AdditionalMentors).filter_by(user_id=mentor.id).first()
            degree = DegreeModel.get_degree_by_id(db, additional_mentor.degree_id).degree_name
            course = CourseModel.get_course_by_id(db, additional_mentor.course_id).course_name

            # Check if the user is involved with this mentor
            accepted_status = db.query(MentorStudent).filter(
                MentorStudent.user_id == user_id,
                MentorStudent.mentor_id == mentor.id,
                MentorStudent.status == 'accepted',
                MentorStudent.completed == False
            ).first()
            
            get_status = db.query(MentorStudent).filter(
                MentorStudent.user_id == user_id,
                MentorStudent.mentor_id == mentor.id,
                MentorStudent.completed == False
            ).first()

            admitted_students = db.query(MentorStudent).filter(
                MentorStudent.mentor_id == mentor.id,
                MentorStudent.admission_progress == 1.0
            ).count()
            
            status = None
            if get_status is not None:
                status = get_status.status if get_status.status != 'rejected' else None
            

            mentor_info = {
                'mentor_id': mentor.id,
                'email': mentor.email_address,
                'first_name': mentor.first_name,
                'last_name': mentor.last_name,
                'is_verified': mentor.is_verified,
                'photo': mentor.photo,
                'created_at': mentor.created_at,
                'accepted': accepted_status is not None,
                'admitted_student': admitted_students,
                'biography': additional_mentor.bio,
                'status': status
            }
            mentors_with_status.append(mentor_info)

        if page:
            # Use fastapi-pagination to paginate the list
            page_offset = Params(page=page, size=page_size)
            return paginate(mentors_with_status, params=page_offset)

        return mentors_with_status 