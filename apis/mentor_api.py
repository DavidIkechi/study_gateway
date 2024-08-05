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
from schemas.user_schema import UserSchema, MentorSchema, UserPasswordSchema, CodeSchema, refreshTokenSchema, ResendEmailSchema
from fastapi.security import OAuth2PasswordRequestForm

from crud import user_crud, mentor_crud


mentor_router = APIRouter(
    prefix="/mentors",
    tags=["Mentors"]
)

@mentor_router.post('', summary="Create a new mentor", status_code=201)
async def create_user(user: MentorSchema, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await user_crud.create_user(db, user, backtask, mentor= True)
        db.commit()
        return success_response.success_message([], f"Mentor {user.email_address} created successfully., A verification mail has been sent to you. In case you didn't receive it, click on button below to resend ", 201)
    
    except BadExceptions as e:
        db.rollback()
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        db.rollback()
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        db.rollback()
        return exceptions.server_error(str(e))

@mentor_router.post('/login', summary="Login a Mentor", status_code=200)
async def login_user(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # get the email and password.
        user_email, user_password = login_data.username, login_data.password
        allow_user = mentor_crud.user_login(db, user_email, user_password)
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

@mentor_router.get('/forgot-password', summary="Forget Mentor's password", status_code=200)
async def send_password(email: str, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await mentor_crud.send_code(db, email, backtask)
        db.commit()
        return success_response.success_message([], f"A password reset code has been sent to your mail. Also check your spam folder.", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    

@mentor_router.post('/verify-code', summary="Verify OTP", status_code=200)
async def verify_code(code: CodeSchema, db: Session = Depends(get_db)):
    try:
        check_code = mentor_crud.verify_code(db, code)
        return success_response.success_message(check_code, detail="Verification Successful")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)

    except Exception as e:
        return exceptions.server_error(detail=str(e))

@mentor_router.patch('/change-password', summary="Change Mentors's password", status_code=200)
async def change_password(token: str, user: UserPasswordSchema, db: Session = Depends(get_db)):
    try:
        check_code = mentor_crud.change_password(db, token, user)
        db.commit()

        return success_response.success_message(detail="Password was successfully changed.")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)

    except Exception as e:
        return exceptions.server_error(detail=str(e))

@mentor_router.post("/refresh-token", summary="Refresh Expired token of logged in Mentors.", status_code=200)
async def refresh_token(refresh_token: refreshTokenSchema, db: Session = Depends(get_db)):
    try:
        user_token = user_crud.refresh_token(db, refresh_token.refresh_token)
        return success_response.success_message(user_token)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@mentor_router.get('', summary="Get active Mentor", status_code=200)
async def get_user(db: Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    try:
        user_detail = mentor_crud.get_user_detail(db, current_user)
        return success_response.success_message(user_detail)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))