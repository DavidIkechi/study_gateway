from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db 
from auth import validate_active_client
from response_handler import error_response as exceptions
from argon2.exceptions import VerifyMismatchError
from response_handler import success_response
from exceptions import (
    BadExceptions, 
    NotFoundException, 
    ServerErrorException, 
    NotAuthorizedException,
    ForbiddenException
)
from schemas.profile_schema import (
    UserInfoSchema, 
    ChangePasswordSchema,
    ContactInfoSchema,
    DegreeSchema
)
from crud import user_profile_crud
     
from fastapi.security import OAuth2PasswordRequestForm

# from crud import user_crud


user_profile_router = APIRouter(
    prefix="/user-profiles",
    tags=["User profiles"]
)

@user_profile_router.patch('/personal-info', summary="Update User personal information", status_code=200)
async def update_personal_info(profile: UserInfoSchema, db: Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    try:
        user_info = user_profile_crud.update_user_info(db, profile, current_user)
        db.commit()
        return success_response.success_message([], f"User {current_user['sub']} personal information was updated successfully", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
@user_profile_router.patch('/contact-info', summary="Update User Contact information", status_code=200)
async def update_personal_info(profile: ContactInfoSchema, db: Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    try:
        user_info = user_profile_crud.update_contact_info(db, profile, current_user)
        db.commit()
        return success_response.success_message([], f"User {current_user['sub']} Contact information was updated successfully", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
@user_profile_router.patch('/degree-info', summary="Update User Degree information", status_code=200)
async def update_personal_info(profile: DegreeSchema, db: Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    try:
        user_info = user_profile_crud.update_degree_info(db, profile, current_user)
        db.commit()
        return success_response.success_message([], f"User {current_user['sub']} Degree information was updated successfully", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))