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
    GenderModel, AdditionalMentors
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