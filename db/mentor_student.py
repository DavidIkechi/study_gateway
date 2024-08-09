from .session import Base

from sqlalchemy import (
    Column, Enum, Integer, String, Boolean,
    BigInteger, TIMESTAMP, ForeignKey, Float,
    JSON, TEXT, LargeBinary, DateTime, Date
)
import uuid
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import func
from fastapi_pagination import paginate, Params


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
    year = Column(Integer, nullable=True)  # Use Date to store the year
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
    def get_ment_studs_by_slug(db: Session, slug):
        return MentorStudent.get_ment_studs_object(db).filter_by(application_ref=slug).first()

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
    
    @staticmethod
    def get_mentors(db: Session, user_id: int, name: str = None, page: int = None, page_size: int = 10, current: bool = False):
        from db.main_model import AdditionalMentors, UserModel, MentorStudent, DegreeModel, CourseModel, ProfileModel, DegreeSoughtModel       
        # Query the mentors associated with the given user_id (mentor_id)
        
        if current is True:
            query = db.query(MentorStudent).join(
                UserModel, UserModel.id == MentorStudent.user_id 
            ).filter(
                MentorStudent.mentor_id == user_id,
                MentorStudent.completed == False,
                MentorStudent.status == 'accepted'
            )
        else:
            query = db.query(MentorStudent).join(
                UserModel, UserModel.id == MentorStudent.user_id 
            ).filter(
                MentorStudent.mentor_id == user_id,
                MentorStudent.status == 'accepted'
            )
                   
        # Apply name filter if provided
        if name is not None:
            name_filter = f"%{name}%"
            query = query.filter(
                (UserModel.first_name + ' ' + UserModel.last_name).ilike(name_filter)
            )
        
        student_info = []
        for stud in query.all():
            mentor = MentorStudent.get_ment_studs_by_id(db, stud.id)
            # Assuming each student has one profile
            degree_name = DegreeModel.get_degree_by_id(db, mentor.degree_id).degree_name
            course_name = CourseModel.get_course_by_id(db, mentor.course_id).course_name
            
            student = UserModel.get_user_by_id(db, mentor.user_id)
            # Extract the necessary information from profile_info
            degree_sought= db.query(DegreeSoughtModel).join(
                ProfileModel, ProfileModel.degree_sought_id == DegreeSoughtModel.id
            ).filter(
                ProfileModel.user_id == stud.user_id
            ).first()
            
            students = {
                'mentor_id': stud.id,
                'email': student.email_address,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'is_verified': student.is_verified,
                'photo': student.photo,
                'created_at': student.created_at,
                'highest_degree': degree_name,
                'degree_sought': degree_sought.degree_name,
                'course_name': course_name
            }
            student_info.append(students)
        
        # Apply pagination if needed
        if page:
            page_offset = Params(page=page, size=page_size)
            return paginate(student_info, params=page_offset)

        return student_info
    
    @staticmethod
    def get_student_info(db, app_id:int):
        from db.main_model import CourseModel, UserModel, DegreeSoughtModel, DegreeModel, ProfileModel, UniversityModel, NationalityModel
        query = MentorStudent.get_ment_studs_by_id(db, app_id)
        user = UserModel.get_user_by_id(db, query.user_id)
        
        degree_sought= db.query(DegreeSoughtModel).join(
                ProfileModel, ProfileModel.degree_sought_id == DegreeSoughtModel.id
            ).filter(
                ProfileModel.user_id == user.id
            ).first()
            
        nat= db.query(NationalityModel).join(
                ProfileModel, ProfileModel.nationality_id == NationalityModel.id
            ).filter(
                ProfileModel.user_id == user.id
            ).first()
        
        details = {
            'name': (user.first_name + ' ' + user.last_name).title(),
            'email_address': user.email_address,
            'course_name': CourseModel.get_course_by_id(db, query.course_id).course_name,
            'degree': DegreeModel.get_degree_by_id(db, query.degree_id).degree_name,
            'degree_sought': degree_sought.degree_name,
            'admission_progress': query.admission_progress,
            'visa_progress': query.visa_progress,
            'year': query.year,
            'mentor_id': query.mentor_id,
            'nationality': nat.nationality,
            'document_progress': query.document_progress,
            'university': UniversityModel.get_university_by_id(db, query.university_id).name
            
        }
        
        return details