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
async def get_user(email_address: str = Query(default=None), db:Session = Depends(get_db), 
                   current_user: dict = Depends(validate_active_client)):
    try:
        user_detail = admin_crud.activate_mentors(db, current_user, email_address)
        db.commit()
        return success_response.success_message("activated successfully")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e)) 