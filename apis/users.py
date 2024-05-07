from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db 
# from auth import validate_active_client
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
from schemas.user_schema import UserSchema, CodeSchema, refreshTokenSchema
from fastapi.security import OAuth2PasswordRequestForm

from crud import user_crud


user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post('', summary="Create a new user", status_code=201)
async def create_user(user: UserSchema, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await user_crud.create_user(db, user, backtask)
        db.commit()
        return success_response.success_message([], f"User {user.email_address} created successfully., A verification mail has been sent to you. In case you didn't receive it, click on button below to resend ", 201)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))

@user_router.post('/login', summary="Login a user", status_code=200)
async def login_user(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # get the email and password.
        user_email, user_password = login_data.username, login_data.password
        allow_user = user_crud.user_login(db, user_email, user_password)
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

@user_router.get('/forget-password', summary="Forget user's password", status_code=200)
async def send_password(email: str, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await user_crud.send_code(db, email, backtask)
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
    

@user_router.post('/verify-code', summary="Verify OTP", status_code=200)
async def verify_code(code: CodeSchema, db: Session = Depends(get_db)):
    try:
        check_code = user_crud.verify_code(db, code)
        return success_response.success_message(check_code, detail="Verification Successful")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)

    except Exception as e:
        return exceptions.server_error(detail=str(e))

@user_router.patch('/change-password', summary="Change user's password", status_code=200)
async def change_password(token: str, user: UserSchema, db: Session = Depends(get_db)):
    try:
        check_code = user_crud.change_password(db, token, user)
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

@user_router.post("/refresh-token", summary="Refresh Expired token of logged in users.", status_code=200)
async def refresh_token(refresh_token: refreshTokenSchema, db: Session = Depends(get_db)):
    try:
        user_token = user_crud.refresh_token(db, refresh_token.refresh_token)
        return success_response.success_message(user_token)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))


@user_router.post('/resend-verification-link', summary="Resend Verification Link", status_code=200)
async def create_user(user: str, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await user_crud.resend_link(db, user, backtask)
        db.commit()
        return success_response.success_message([], f"A link has been sent to {user.email_address}", 201)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))

@user_router.post("/verify-email-token", summary="Verify Token from Email Verification Link.", status_code=200)
async def refresh_token(refresh_token: refreshTokenSchema, db: Session = Depends(get_db)):
    try:
        user_account = user_crud.verify_token(db, refresh_token.refresh_token)
        db.commit()
        return success_response.success_message([], f"Account has been successfully verified")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))