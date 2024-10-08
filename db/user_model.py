from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, BigInteger, TIMESTAMP, ForeignKey, Float, JSON, TEXT, LargeBinary, DateTime
from sqlalchemy.orm import Session, load_only, relationship, joinedload

import uuid
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import and_, not_, or_
from fastapi_pagination.ext.sqlalchemy import paginate as pg
from fastapi_pagination import Params, paginate
import random

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
    photo = Column(TEXT, nullable=True)  # Add photo column
    reason = Column(TEXT, nullable=True) 

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
            UserModel.is_setup,
            UserModel.first_name,
            UserModel.last_name
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
                'course': course,
                'degree': degree,
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
    
    
    @staticmethod
    def get_schools(db: Session, uni_id: int = None, loc_id: int = None, course: str=None, page: int = None, page_size: int = 10):
        from db.main_model import CourseModel, UniversityModel, UniversityDescription, DegreeTypeModel, CollegeSchoolModel, StateUniversityModel, LocationModel
        
        query = db.query(UniversityDescription)
        if uni_id is not None:
            query = query.filter(UniversityDescription.university_id == uni_id)
            
        if loc_id is not None:
            query = query.filter(UniversityDescription.state_id == loc_id)
        # Build the query
        if course is not None:
            matching_courses = db.query(CourseModel.id).filter(CourseModel.course_name.ilike(f'%{course}%')).subquery()
            # Filter the UniversityDescription records by the matching course IDs
            query = query.filter(UniversityDescription.course_id.in_(matching_courses))
        
        # Build a list of schools
        schools = []
        for school in query.all():
            coursename = db.query(CourseModel).get(school.course_id).course_name
            desc = school.description
            state_name = db.query(StateUniversityModel).get(school.state_id).name
            uni_name = db.query(UniversityModel).get(school.university_id).name
            college_name = db.query(CollegeSchoolModel).get(school.college_id).name
            location = db.query(LocationModel).filter(LocationModel.university_id == school.university_id).first()
            image_url = random.choice(location.image_urls) if location and location.image_urls else None
            slug = school.slug
            # Check if the user is involved with this mentor            
            school_info = {
                'school_id': school.id,
                'slug': slug,
                'school_description': desc,
                'state_name': state_name,
                'school_name': uni_name,
                'image_url': image_url,
                'course_name': coursename,
                'college': college_name,
                'academic_level': school.academic_level
            }
            schools.append(school_info)

        if page:
            # Use fastapi-pagination to paginate the list
            page_offset = Params(page=page, size=page_size)
            return paginate(schools, params=page_offset)

        return schools
    
    @staticmethod
    def get_school_details(db: Session, uni_id: int):
        from db.main_model import CourseModel, UniversityModel, UniversityDescription, DegreeTypeModel, CollegeSchoolModel, StateUniversityModel, LocationModel
        
        school = db.query(UniversityDescription).get(uni_id)        
        # Build a list of schools
        
        coursename = db.query(CourseModel).get(school.course_id).course_name
        desc = school.description
        state_name = db.query(StateUniversityModel).get(school.state_id).name
        uni_name = db.query(UniversityModel).get(school.university_id).name
        college_name = db.query(CollegeSchoolModel).get(school.college_id).name
        location = db.query(LocationModel).filter(LocationModel.university_id == school.university_id).first()
        image_url = location.image_urls if location and location.image_urls else None
        slug = school.slug
        tuition = school.tuition
        uni_detail = db.query(UniversityModel).get(school.university_id)
        latitude = location.latitude if location else None
        longitude = location.longitude if location else None

        # Retrieve all unique phone numbers for the given university_id
        phone_numbers = db.query(UniversityDescription.phone_number).filter(
            UniversityDescription.university_id == school.university_id
        ).distinct().all()
        
        # Extract the phone numbers from the query result
        phone_numbers = [phone for phone in phone_numbers]

            # Check if the user is involved with this mentor            
        school_info = {
            'school_id': school.id,
            'school_description': desc,
            'state_name': state_name,
            'school_name': uni_name,
            'image_url': image_url,
            'course_name': coursename,
            'college': college_name,
            'academic_level': school.academic_level,
            'tuition': tuition,
            'address': uni_detail.address,
            'website_link': uni_detail.url,
            'latitude': latitude,
            'longitude': longitude,
            'phone_number': phone_numbers
        }

        return school_info
    
    @staticmethod
    def all_mentors_students(db: Session, is_mentor: bool = False, status: bool=None, name: str= None, page: int = None, page_size: int = 10):
        from db.main_model import AdditionalMentors, MentorStudent, DegreeModel, CourseModel
        # Build the query
        query = db.query(UserModel).filter(
            UserModel.is_mentor == is_mentor,
            UserModel.is_admin == False
        )
        if status is not None:
            query = query.filter(UserModel.is_setup == status)
        # Apply name filter if provided
        if name is not None:
            name_filter = f"%{name}%"
            query = query.filter(
                (UserModel.first_name + ' ' + UserModel.last_name).ilike(name_filter)
            )
        mentors_with_status = []
        for mentor in query.all():
            mentor_info = {
                'mentor_id': mentor.id,
                'email': mentor.email_address,
                'first_name': mentor.first_name,
                'last_name': mentor.last_name,
                'is_verified': mentor.is_verified,
                'photo': mentor.photo,
                'is_active': mentor.is_setup
            }
            mentors_with_status.append(mentor_info)

        if page:
            # Use fastapi-pagination to paginate the list
            page_offset = Params(page=page, size=page_size)
            return paginate(mentors_with_status, params=page_offset)

        return mentors_with_status
    
    @staticmethod
    def mentor_student_count(db: Session):
        query = db.query(UserModel).filter(
            UserModel.is_admin == False,
        )
        all_students = query.filter(
            UserModel.is_mentor == False
        )
        
        all_mentors = query.filter(
            UserModel.is_mentor == True
        )
        
        in_active_mentors = all_mentors.filter(
            UserModel.is_setup == False
        )
        
        return {
            'all_students': all_students.count(),
            'all_mentors': all_mentors.count(),
            'in_active_mentors': in_active_mentors.count()
        }
        
    @staticmethod
    def user_profile(db: Session):
        query = db.query(UserModel).filter(
            UserModel.is_admin == False,
        )
        all_students = query.filter(
            UserModel.is_mentor == False
        )
        
        all_mentors = query.filter(
            UserModel.is_mentor == True
        )
        
        in_active_mentors = all_mentors.filter(
            UserModel.is_setup == False
        )
        
        return {
            'all_students': all_students.count(),
            'all_mentors': all_mentors.count(),
            'in_active_mentors': in_active_mentors.count()
        }
        
