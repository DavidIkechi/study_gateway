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
    GenderModel, AdditionalMentors, AdditionalMentors, LanguageModel, MentorStudent,
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

def check_mentor_slug(db, slug):
    get_info = MentorStudent.get_ment_studs_by_slug(db, slug)
    if get_info is None:
        raise NotFoundException(f"Application Reference not found.")
    return get_info

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

def is_mentor(check_user, login=False):
    if login:
        if not check_user.is_mentor:
            raise ForbiddenException("Not permitted to access this resource, contact admin or support")
    if not check_user.is_mentor:
        raise NotAuthorizedException("Not a mentor, contact admin or support")
    
    return check_user

def user_login(db, email, password):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = is_mentor(check_user, True)
    
    return user_crud.user_login(db, email, password)

async def send_code(db, email: str, backtasks):
    # first check if email_address exists.
    check_user = check_mail(db, email)
    _ = is_mentor(check_user)
    
    return await user_crud.send_code(db, email, backtasks)

def verify_code(db, code):
     # first check if email_address exists.
    check_user = check_mail(db, code.email_address)
    _ = is_mentor(check_user)
    
    return user_crud.verify_code(db, code)

def change_password(db, token, user):
    # check to see if the email address already exists
    bool_result, token_data = password_verif_token(token)

    if not bool_result:
        raise BadExceptions(token_data)
    
    check_user =  check_mail(db, token_data)
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
    get_user = UserModel.get_user_object(db).filter_by(id=user_id).first()
    query = UserModel.get_user_object(db).filter_by(id=user_id)
    _ = is_mentor(query.first())
    
    query = query.options(
            # Load only specific fields for the main entity
            load_only(
                'id',
                'email_address',
                'first_name',
                'last_name',
                'created_at',
                'is_setup',
                'is_verified',
                'photo',
                'id'
            ),
        joinedload(UserModel.user_profiles).load_only(ProfileModel.id, ProfileModel.city, ProfileModel.address, 
                                                      ProfileModel.phone, ProfileModel.zip_code, ProfileModel.birth_date),
        joinedload(UserModel.mentors).load_only(AdditionalMentors.id, AdditionalMentors.address, AdditionalMentors.birth_date, AdditionalMentors.bio),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.genders).load_only('id','slug','name'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.languages).load_only('id', 'name', 'slug'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.degrees).load_only('id', 'degree_name', 'slug'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.nationalities).load_only('id', 'nationality', 'slug'),
        joinedload(UserModel.mentors).joinedload(AdditionalMentors.courses).load_only('id','course_name', 'slug')
    )

    user_profile = {
        'user': query.first()
    }
    
    return user_profile

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
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    
    _ = is_mentor(get_user)
    
    return user_profile_crud.change_photo(db, profile_info, current_user)

def get_overview(db, current_user):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)

    _ = is_mentor(get_user)

    # Retrieve the count of all students associated with the mentor
    all_students = db.query(MentorStudent).filter(
        MentorStudent.mentor_id == user_id,
        MentorStudent.status == 'accepted'
    ).count()

    # Retrieve the count of current students
    current_students = db.query(MentorStudent).filter(
        MentorStudent.mentor_id == user_id,
        MentorStudent.status == 'accepted',
        MentorStudent.completed == False,
        MentorStudent.admission_progress != 1.0
    ).count()

    # Retrieve the count of successful students
    successful_students = db.query(MentorStudent).filter(
        MentorStudent.mentor_id == user_id,
        MentorStudent.status == 'accepted',
        MentorStudent.admission_progress == 1.0
    ).count()

    return {
        "all_students": all_students,
        "current_students": current_students,
        "successful_admissions": successful_students
    }
    
def check_mentor_stud(db, ment_slug):
    mentor = MentorStudent.get_ment_studs_by_slug(db, ment_slug)
    if not mentor:
        raise NotFoundException(f"Sorry, application reference not found")
    
    return mentor
    
async def accept_or_decline(db, current_user, details, backtask):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)

    _ = is_mentor(get_user)
    get_mentor = check_mentor_stud(db, details.connect_ref)
    if get_mentor.mentor_id != user_id:
        raise BadExceptions(f"Connection request not tied to mentor")
    
    student = UserModel.get_user_by_id(db, get_mentor.user_id)
    
    if get_mentor.status == 'accepted':
        raise BadExceptions(f"Connection already accepted")    
    # Delete other connections and set the current connection status to accepted
    db.query(MentorStudent).filter(
        MentorStudent.user_id == get_mentor.user_id,
        MentorStudent.mentor_id != user_id,
        MentorStudent.degree_id == get_mentor.degree_id,
        MentorStudent.course_id == get_mentor.course_id,
        MentorStudent.year == get_mentor.year,
        MentorStudent.status != 'accepted',
    ).delete()
    
    status = 'accepted' if details.status else 'rejected'
    
    get_mentor.status = status
    
    await connection_email(student, get_user, backtask)
    
    return True

def get_students(db, current_user, name: str, page:int = None, page_size:int=None, current: bool= False):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_mentor(get_user)
    
    return MentorStudent.get_mentors(db, user_id, name, page, page_size, current)

def more_details(db, app_id: int):
    return MentorStudent.get_student_info(db, app_id)

def get_more_detail(db, current_user, ment_slug):
    from crud.user_crud import check_mail
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_mentor(get_user)
    
    get_application = check_mentor_slug(db, ment_slug)
    # check if the email.id is 
    if get_application.mentor_id != user_id:
        raise BadExceptions(f"Mentor not tied to student")

    return more_details(db, get_application.id) 
    
def update_admission(db, current_user, connection_slug, profile):
    from crud.settings import check_courses_by_slug, check_university_by_slug, check_degree_by_slug
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_mentor(get_user)
    
    get_application = check_mentor_slug(db, connection_slug)
    # check if the email.id is 
    if get_application.mentor_id != user_id:
        raise BadExceptions(f"Mentor not tied to student")
    
    profile_dict = profile.dict(exclude_none=True)
   # Update university if provided and pop it from the dictionary
    if 'university' in profile_dict:
        profile_dict['university_id'] = check_university_by_slug(db, profile_dict.pop('university')).id
    # Update course if provided and pop it from the dictionary
    if 'course' in profile_dict:
        profile_dict['course_id'] = check_courses_by_slug(db, profile_dict.pop('course')).id
    # Update degree if provided and pop it from the dictionary
    if 'degree' in profile_dict:
        profile_dict['degree_id'] = check_degree_by_slug(db, profile_dict.pop('degree')).id
        
    return MentorStudent.update_ment_studs(db, get_application.id, profile_dict)

def get_students_request(db, current_user, name: str, page:int = None, page_size:int=None):
    user_id = current_user.get('user_id')
    get_user = UserModel.get_user_by_id(db, user_id)
    _ = is_mentor(get_user)
    
    return MentorStudent.get_mentors_request(db, user_id, name, page, page_size)

    
    
    
    
    
    