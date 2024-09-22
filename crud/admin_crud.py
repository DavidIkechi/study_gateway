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
    GenderModel, AdditionalMentors, AdditionalMentors, LanguageModel, MentorStudent
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
from crud import user_crud, user_profile_crud


hasher = PasswordHasher()

def check_mail(db, email, new_user= False):
    get_user = UserModel.check_email(db, email)
    if new_user:
        if get_user is not None:
            raise BadExceptions(detail=f"Email {email} already in use.")
    else:
        if get_user is None:
            raise NotFoundException(detail=f"User with this email {email} does not exist.")
        
    return get_user

def is_admin(check_user):
    if not check_user.is_admin:
        raise BadExceptions("Not an admin, contact support")
    
    return check_user

def user_login(db, email, password):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = is_admin(check_user)
    
    return user_crud.user_login(db, email, password)

async def activate_mentor(db, email_address, backtasks):
    from crud.mentor_crud import is_mentor
    check_user = check_mail(db, email_address)
    check_mentor = is_mentor(check_user)
    
    if check_mentor.is_setup:
        raise BadExceptions(f"mentor {email_address} already verified!")

    check_mentor.is_setup = True
    await send_mentor_verification_email(check_user, backtasks)

    return check_mentor

async def reject_mentor(db, current_user, backtasks, mentor_reason):
    from crud.mentor_crud import is_mentor
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
    
    check_user = check_mail(db, mentor_reason.email_address)
    check_mentor = is_mentor(check_user)
    
    if check_mentor.is_setup:
        raise BadExceptions(f"mentor {email_address} already verified!")

    check_mentor.is_setup = False
    if check_mentor.reason is None:
        check_mentor.reason = ""
        
    if mentor_reason.reason is None:
        mentor_reason.reason = ""
        
    check_mentor.reason += "<br>" + mentor_reason.reason
    await send_mentor_rejection_email(check_user, backtasks, mentor_reason.reason)

    return check_mentor

async def activate_mentors(db, current_user,  backtasks, email_address: str = None):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
    
    if email_address is not None:
        return await activate_mentor(db, email_address, backtasks)
    
    updated_count = db.query(UserModel).filter(
        UserModel.is_mentor == True,
        UserModel.is_setup == False
    ).update(
        {UserModel.is_setup: True},
        synchronize_session=False
    )
    
    return updated_count

def get_mentors(db, current_user, status: bool=None, search: str=None, page: int=None, page_size:int = None):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
        
    return UserModel.all_mentors_students(db, True, status, search, page, page_size)

def get_mentor_student(db, current_user):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
    
    return UserModel.mentor_student_count(db)

def get_students(db, current_user, status: bool=None, search: str=None, page: int=None, page_size:int = None):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
        
    return UserModel.all_mentors_students(db, False, status, search, page, page_size)

def get_mentor_student_count(db, current_user):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
    
    return UserModel.mentor_student_count(db)

def get_user_info(db, current_user, email_address: str):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
    
    query = UserModel.get_user_object(db).filter_by(email_address=email_address)
    
    query = query.options(
        load_only(UserModel.id, UserModel.photo, UserModel.email_address, UserModel.first_name, UserModel.last_name, UserModel.created_at,
                  UserModel.is_setup, UserModel.is_verified),
        joinedload(UserModel.user_profiles).load_only(ProfileModel.id, ProfileModel.city, ProfileModel.address, 
                                                      ProfileModel.phone, ProfileModel.zip_code, ProfileModel.birth_date),
        joinedload(UserModel.user_profiles).joinedload(ProfileModel.genders).load_only('id','slug','name'),
        joinedload(UserModel.user_profiles).joinedload(ProfileModel.countries).load_only('id', 'country_name', 'slug'),
        joinedload(UserModel.user_profiles).joinedload(ProfileModel.states).load_only('id', 'name', 'slug'),
        joinedload(UserModel.user_profiles).joinedload(ProfileModel.degrees).load_only('id', 'degree_name', 'slug'),
        joinedload(UserModel.user_profiles).joinedload(ProfileModel.degree_soughts).load_only('id', 'degree_name', 'slug'),
        joinedload(UserModel.user_profiles).joinedload(ProfileModel.nationalities).load_only('id', 'nationality', 'slug'),
        joinedload(UserModel.user_profiles).joinedload(ProfileModel.courses).load_only('id','course_name', 'slug'),
        joinedload(UserModel.user_details).load_only('id', 'email_address2', 'address2', 
                                                     'course_extra', 'highest_degree_extra')
    )
    
    return query.first()