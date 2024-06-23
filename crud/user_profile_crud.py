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
    GenderModel
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

hasher = PasswordHasher()

def create_user_profile(db, user_id: int):
    user_profile = ProfileModel.create_profile({'user_id': user_id})
    db.add(user_profile)
    
    additional_details = AdditionalUserDetails.create_user_details({'user_id': user_id})
    db.add(additional_details)
    
    return True

def check_profile(db, user_id):
    user = ProfileModel.get_profile_by_user_id(db, user_id)
    if any(value is None for value in user.__dict__.values()):
        return UserModel.update_user(db, user_id, {'is_setup': False})
    return UserModel.update_user(db, user_id, {'is_setup': True})
    
def update_user_info(db, profile_info, current_user):
    from crud.settings import check_gender_by_slug, check_nationality_by_slug
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    
    profile_id = ProfileModel.get_profile_by_user_id(db, user_id).id
    
    if info_dict.get('gender') is not None:
        info_dict['gender_id'] = check_gender_by_slug(db, info_dict['gender']).id
        info_dict.pop('gender')
    
    if info_dict.get('nationality') is not None:
        info_dict['nationality_id'] = check_nationality_by_slug(db, info_dict['nationality']).id
        info_dict.pop('nationality')
        
    user_record = NameSchema(**{'first_name': info_dict.get('first_name'),
                                'last_name': info_dict.get('last_name')}).dict(exclude_none=True)
        
    update = ProfileModel.update_profile(db, profile_id, info_dict)
    update_user = UserModel.update_user(db, user_id, user_record)
    db.flush()
    return check_profile(db, user_id)

def update_contact_info(db, profile_info, current_user):
    from crud.settings import check_country_by_slug, check_states_by_slug
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    
    profile_id = ProfileModel.get_profile_by_user_id(db, user_id).id
    details_id = AdditionalUserDetails.get_user_details_by_user_id(db, user_id).id
    
    if info_dict.get('country') is not None:
        info_dict['country_id'] = check_country_by_slug(db, info_dict['country']).id
        info_dict.pop('country')
    
    if info_dict.get('state') is not None:
        info_dict['state_id'] = check_states_by_slug(db, info_dict['state']).id
        info_dict.pop('state')
                
    extra_record = ExtraSchema(**{'email_address2': info_dict.get('email_address'),
                                'address2': info_dict.get('address2')}).dict(exclude_none=True)
        
    update = ProfileModel.update_profile(db, profile_id, info_dict)
    update_user = AdditionalUserDetails.update_user_details(db, details_id, extra_record)
    db.flush()
    return check_profile(db, user_id)

def update_degree_info(db, profile_info, current_user):
    from crud.settings import check_courses_by_slug, check_sought_by_slug, check_degree_by_slug
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    
    profile_id = ProfileModel.get_profile_by_user_id(db, user_id).id
    details_id = AdditionalUserDetails.get_user_details_by_user_id(db, user_id).id
    
    if info_dict.get('degree') is not None:
        info_dict['degree_id'] = check_degree_by_slug(db, info_dict['degree']).id
        info_dict.pop('degree')
        
    if info_dict.get('courses') is not None:
        info_dict['course_id'] = check_courses_by_slug(db, info_dict['courses']).id
        info_dict.pop('courses')
    
    if info_dict.get('degree_sought') is not None:
        info_dict['degree_sought_id'] = check_sought_by_slug(db, info_dict['degree_sought']).id
        info_dict.pop('degree_sought')
                
    extra_record = ExtraSchema(**{'course_extra': info_dict.get('course_extra'),
                                'highest_degree_extra': info_dict.get('highest_degree_extra')}).dict(exclude_none=True)
        
    update = ProfileModel.update_profile(db, profile_id, info_dict)
    update_user = AdditionalUserDetails.update_user_details(db, details_id, extra_record)
    db.flush()
    return check_profile(db, user_id)

def change_password(db, profile_info, current_user):
    # check to see if the email address already exists
    info_dict = profile_info.dict(exclude_none=True)
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)

    # check passwords.
    get_password = profile_info.current_password
    new_password = profile_info.new_password
    
    if hasher.verify(get_user.password, get_password):
        bool, message = check_password(new_password)
        if not bool:
            raise BadExceptions(detail=message)
        
        get_user.password = hasher.hash(new_password)
    
    return get_user

def get_user_profile(db, current_user):
    user_id = current_user.get('user_id')
    query = UserModel.get_user_object(db).filter_by(id=user_id)
    
    query = query.options(
        load_only(UserModel.id, UserModel.email_address, UserModel.first_name, UserModel.last_name),
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