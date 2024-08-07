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
    GenderModel, AdditionalMentors, AdditionalMentors, LanguageModel
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

def create_mentor(db, mentor_data, user_id: int):
    from crud.settings import check_gender_by_slug, check_nationality_by_slug, check_courses_by_slug, check_degree_by_slug, check_language_by_slug
    mentor_dict = {
        'language_id': check_language_by_slug(db, mentor_data['language']).id,
        'course_id': check_courses_by_slug(db, mentor_data['course']).id,
        'gender_id': check_gender_by_slug(db, mentor_data['gender']).id,
        'nationality_id': check_nationality_by_slug(db, mentor_data['nationality']).id,
        'degree_id': check_degree_by_slug(db, mentor_data['degree']).id,
    }
    
    profile_dict = {
        'user_id': user_id,'course_id': check_courses_by_slug(db, mentor_data['course']).id,
        'gender_id': check_gender_by_slug(db, mentor_data['gender']).id,
        'nationality_id': check_nationality_by_slug(db, mentor_data['nationality']).id,
        'degree_id': check_degree_by_slug(db, mentor_data['degree']).id
    }
    if mentor_data.get('birth_date') is not None:
        mentor_dict['birth_date'] = mentor_data['birth_date']
        profile_dict['birth_date'] = mentor_data['birth_date']
        
    user_profile = ProfileModel.create_profile(profile_dict)
    db.add(user_profile)
    
    additional_details = AdditionalUserDetails.create_user_details({'user_id': user_id})
    db.add(additional_details)
    
    mentor_dict['user_id'] = user_id
    additional_mentors = AdditionalMentors.create_mentors(mentor_dict)
    db.add(additional_mentors)
    
    return True

def is_mentor(check_user):
    if not check_user.is_mentor:
        raise BadExceptions("Not a mentor, contact admin or support")
    
    return check_user

def user_login(db, email, password):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = is_mentor(check_user)
    
    return user_crud.user_login(db, email, password)

async def send_code(db, email: str, backtasks):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = is_mentor(check_user)
    
    return user_crud.send_code(db, email, backtasks)

def verify_code(db, code):
     # first check if email_address exists.
    check_user = check_mail(db, code.email_address)
    _ = is_mentor(check_user)
    
    return user_crud.verify_code(db, code)

def change_password(db, token, user):
    # check to see if the email address already exists
    check_user =  check_mail(db, user.email_address)
    _ = is_mentor(check_user)
    
    return user_crud.change_password(db, token, user)

def get_user_by_email(db, email_address):
    get_email = check_mail(db, email_address)
    return UserModel.get_user_by_email(db, email_address)

def get_user_detail(db, user_dict):
    email_address = user_dict.get('sub')
    return get_user_by_email(db, email_address)

def get_user_details(db, current_user):
    user_id = current_user.get('user_id')
    query = UserModel.get_user_object(db).filter_by(id=user_id)
    _ = is_mentor(query.first())
    
    query = query.options(
            # Load only specific fields for the main entity
            load_only(
                'id',
                'email_address',
                'first_name',
                'last_name',
                'created_at'
            ),
        joinedload(UserModel.user_profiles).load_only(ProfileModel.id, ProfileModel.city, ProfileModel.address, 
                                                      ProfileModel.phone, ProfileModel.zip_code, ProfileModel.birth_date),
        joinedload(UserModel.mentors).load_only(AdditionalMentors.id, AdditionalMentors.address, AdditionalMentors.birth_date),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.genders).load_only('id','slug','name'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.languages).load_only('id', 'name', 'slug'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.degrees).load_only('id', 'degree_name', 'slug'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.nationalities).load_only('id', 'nationality', 'slug'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.courses).load_only('id','course_name', 'slug')
    )

    return query.first()

def update_user_info(db, profile_info, current_user):
    from crud.settings import check_gender_by_slug, check_nationality_by_slug
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    
    _ = is_mentor(get_user)
    
    return user_profile_crud.update_user_info(db, profile_info, current_user)

def update_contact_info(db, profile_info, current_user):
    from crud.settings import check_country_by_slug, check_states_by_slug
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    
    _ = is_mentor(get_user)
    
    return user_profile_crud.update_contact_info(db, profile_info, current_user)

def update_degree_info(db, profile_info, current_user):
    from crud.settings import check_courses_by_slug, check_sought_by_slug, check_degree_by_slug
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    
    get_user = UserModel.get_user_by_id(db, user_id)
    
    _ = is_mentor(get_user)
    
    return user_profile_crud.update_degree_info(db, profile_info, current_user)

def update_password(db, profile_info, current_user):
    # check to see if the email address already exists
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    
    _ = is_mentor(get_user)
    
    return user_profile_crud.change_password(db, profile_info, current_user)

def change_photo(db, profile_info, current_user):
    # check to see if the email address already exists
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    
    _ = is_mentor(get_user)
    
    return user_profile_crud.change_photo(db, profile_info, current_user)
    