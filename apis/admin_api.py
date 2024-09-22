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
from schemas.user_schema import (
    UserSchema, 
    MentorSchema, 
    UserPasswordSchema, 
    CodeSchema, 
    refreshTokenSchema, 
    ResendEmailSchema,
    ChangeProfileImageSchema,
    ConnectSchema
)
from schemas.profile_schema import (
    UserInfoSchema, 
    ChangePasswordSchema,
    ContactInfoSchema,
    DegreeSchema
)

from fastapi.security import OAuth2PasswordRequestForm

from crud import user_crud, admin_crud


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.post('/login', summary="Login an admin", status_code=200)
async def login_user(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # get the email and password.
        user_email, user_password = login_data.username, login_data.password
        allow_user = admin_crud.user_login(db, user_email, user_password)
        # db.commit()
        return success_response.success_message(allow_user)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)
    
    except VerifyMismatchError as e:
        # update_user_lock =user_crud.initiate_lock(db, request.state.data, login_data.username)
        # db.commit()
        # db.refresh(update_user_lock)
        return exceptions.bad_request_error(detail="Incorrect Username or Password")
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
@admin_router.patch('/mentors/activation', summary="activate mentors", status_code=200)
async def get_user(backtask: BackgroundTasks, email_address: str = Query(default=None), db:Session = Depends(get_db),
                   current_user: dict = Depends(validate_active_client)):
    try:
        await admin_crud.activate_mentors(db, current_user, backtask, email_address)
        db.commit()
        return success_response.success_message("activated successfully")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e)) 
    
@admin_router.get('/mentors', summary="get all mentors or query for active and inactive", status_code=200)
async def get_user(status: bool = Query(default=None), search: str = Query(default=None), page: int= Query(default=None, ge=1),
                   page_size: int=10, db:Session = Depends(get_db), 
                   current_user: dict = Depends(validate_active_client)):
    try:
        all_mentors = admin_crud.get_mentors(db, current_user, status, search, page, page_size)
        return success_response.success_message(all_mentors)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e)) 
    
@admin_router.get('/students', summary="get all students or query for active and inactive", status_code=200)
async def get_user(status: bool = Query(default=None), search: str = Query(default=None), page: int= Query(default=None, ge=1),
                   page_size: int=10, db:Session = Depends(get_db), 
                   current_user: dict = Depends(validate_active_client)):
    try:
        all_students = admin_crud.get_students(db, current_user, status, search, page, page_size)
        return success_response.success_message(all_students)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@admin_router.get('/student-mentor-count', summary="count for student, mentor and inactive mentors", status_code=200)
async def get_user(db:Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    try:
        all_students = admin_crud.get_mentor_student_count(db, current_user)
        return success_response.success_message(all_students)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@admin_router.get('/user-info/{email}', summary="get user information", status_code=200)
async def get_user(email: str, db:Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    try:
        user = admin_crud.get_user_info(db, current_user, email)
        return success_response.success_message(user)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e)) 