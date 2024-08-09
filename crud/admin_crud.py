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

def activate_mentor(db, email_address):
    from crud.mentor_crud import is_mentor
    check_user = check_mail(db, email_address)
    check_mentor = is_mentor(db, check_user)
    check_mentor.is_setup = True
    
    return check_mentor

def activate_mentors(db, current_user, email_address: str = None):
    user_id = cuurent_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_admin(get_user)
    
    
    if email_address is not None:
        return activate_mentor(db, email)
    
    updated_count = db.query(UserModel).filter(
        UserModel.is_mentor == True,
        UserModel.is_setup == False
    ).update(
        {UserModel.is_setup: True},
        synchronize_session=False
    )
    
    return updated_count    