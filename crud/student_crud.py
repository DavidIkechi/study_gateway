import sys
sys.path.append("..")
from utils import *
from db.session import Session
from sqlalchemy.orm import Session, load_only, relationship, joinedload
from exceptions import (
    BadExceptions, 
    NotFoundException, 
    ServerErrorException, 
    NotAuthorizedException,
    ForbiddenException
)
from db.main_model import (
    ProfileModel, AdditionalUserDetails, UserModel,
    GenderModel, AdditionalMentors, MentorStudent
)

from argon2 import PasswordHasher
from send_mail import *
from auth_token import *
import pyotp
from datetime import datetime, timedelta
from simpleotp import OTP
from schemas.user_schema import NameSchema
from schemas.profile_schema import ExtraSchema
import os
from crud import user_crud

def is_mentor_admin(check_user):
    if check_user.is_mentor or check_user.is_admin:
        raise BadExceptions("Only restricted to Student contact admin or support")
    
    return check_user

def check_mail(db, email, new_user= False):
    get_user = UserModel.check_email(db, email)
    if new_user:
        if get_user is not None:
            raise BadExceptions(detail=f"Email {email} already in use.")
    else:
        if get_user is None:
            raise NotFoundException(detail=f"User with this email {email} does not exist.")
        
    return get_user

def user_login(db, email, password):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = is_mentor_admin(check_user)
    
    return user_crud.user_login(db, email, password)

async def send_code(db, email: str, backtasks):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = is_mentor_admin(check_user)
    
    return user_crud.send_code(db, email, backtasks)

def verify_code(db, code):
     # first check if email_address exists.
    check_user = check_mail(db, code.email_address)
    _ = is_mentor_admin(check_user)
    
    return user_crud.verify_code(db, code)

def change_password(db, token, user):
    # check to see if the email address already exists
    check_user =  check_mail(db, user.email_address)
    _ = is_mentor_admin(check_user)
    
    return user_crud.change_password(db, token, user)

def get_user_by_email(db, email_address):
    get_email = check_mail(db, email_address)
    return UserModel.get_user_by_email(db, email_address)

def get_user_detail(db, user_dict):
    email_address = user_dict.get('sub')
    return get_user_by_email(db, email_address)

def get_user_detail(db, current_user):
    user_id = current_user.get('user_id')
    query = UserModel.get_user_object(db).filter_by(id=user_id)
    _ = is_mentor_admin(query.first())
    
    return user_crud.get_user_detail(db, current_user)

def get_mentors(db, current_user, language: str=None, discipline: str=None, page: int=None, page_size:int = None):
    from crud.settings import check_language_by_slug, check_courses_by_slug
    user_id = current_user.get('user_id')
    query = UserModel.get_user_object(db).filter_by(id=user_id)
    _ = is_mentor_admin(query.first())
    language_id, course_id = None, None
    if language is not None:
        language_id = check_language_by_slug(db, language).id
    if discipline is not None:
        course_id = check_courses_by_slug(db, discipline).id
        
    return UserModel.get_mentors(db, user_id, language_id, course_id, page, page_size)

def check_mentor(db, email):
    check_user = check_mail(db, email)
    if not check_user.is_mentor:
        raise BadExceptions(f"{email} does not belong to a mentor")
    if not check_user.is_verified:
        raise BadExceptions(f"Mentor {email} is not verified")
    if not check_user.is_setup:
        raise BadExceptions(f"Mentor {email} is not active, contact admin")
    
    return check_user
    

def send_connection(db, current_user, details):
    from crud.settings import check_university_by_slug
    user_id = current_user.get('user_id')
    query = UserModel.get_user_object(db).filter_by(id=user_id)
    _ = is_mentor_admin(query.first())
    
    details_dict = details.dict(exclude_none=True)
    #check if the email belongs to a mentor.
    email_address = details_dict.get('mentor_email_address')
    mentor = check_mentor(db, email_address).id
    
    year = details_dict.get('year')
    # get the student course
    
    # degree_id, course_id, status, completed
    student_profile = ProfileModel.get_profile_object(db).filter(
        ProfileModel.user_id == user_id).first()
    
    check_request_1 = MentorStudent.get_ment_studs_object(db).filter(
        MentorStudent.user_id == user_id,
        MentorStudent.mentor_id == mentor,
        MentorStudent.degree_id == student_profile.degree_id,
        MentorStudent.course_id == student_profile.course_id,
        MentorStudent.completed == False,
        MentorStudent.year == year
    ).count()
    
    if check_request_1 != 0:
        raise BadExceptions(f"You already sent a connection request initially")

    
    check_request = MentorStudent.get_ment_studs_object(db).filter(
        MentorStudent.user_id == user_id,
        MentorStudent.degree_id == student_profile.degree_id,
        MentorStudent.course_id == student_profile.course_id,
        MentorStudent.status == 'accepted',
        MentorStudent.completed == False,
        MentorStudent.year == year
    ).count()
    
    if check_request != 0:
        raise BadExceptions(f"You are already connected to a mentor, contact admin to change")
    
    new_ment_data = {
        'user_id': user_id,
        'mentor_id': mentor,
        'year': year,
        'degree_id': student_profile.degree_id,
        'course_id': student_profile.course_id,
        'university_id': check_university_by_slug(db, details_dict.get('university')).id
    }
    
    add_data = MentorStudent.create_ment_studs(new_ment_data)
    db.add(add_data)
    
    return add_data
    