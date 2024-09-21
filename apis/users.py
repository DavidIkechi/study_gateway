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
    UserSchema, UserPasswordSchema, 
    CodeSchema, refreshTokenSchema, 
    ResendEmailSchema, UserConnectSchema
)
from fastapi.security import OAuth2PasswordRequestForm

from crud import user_crud, student_crud


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
        db.rollback()
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        db.rollback()
        return exceptions.not_found_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
        
    except Exception as e:
        db.rollback()
        return exceptions.server_error(str(e))

@user_router.post('/login', summary="Login a user", status_code=200)
async def login_user(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # get the email and password.
        user_email, user_password = login_data.username, login_data.password
        allow_user = student_crud.user_login(db, user_email, user_password)
        # db.commit()
        return success_response.success_message(allow_user)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)
    
    except VerifyMismatchError as e:
        # update_user_lock =user_crud.initiate_lock(db, request.state.data, login_data.username)
        # db.commit()
        # db.refresh(update_user_lock)
        return exceptions.bad_request_error(detail="Incorrect Username or Password")
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))

@user_router.get('/forgot-password', summary="Forget user's password", status_code=200)
async def send_password(email: str, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await student_crud.send_code(db, email, backtask)
        db.commit()
        return success_response.success_message([], f"A password reset code has been sent to your mail. Also check your spam folder.", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    

@user_router.post('/verify-code', summary="Verify OTP", status_code=200)
async def verify_code(code: CodeSchema, db: Session = Depends(get_db)):
    try:
        check_code = student_crud.verify_code(db, code)
        return success_response.success_message(check_code, detail="Verification Successful")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)

    except Exception as e:
        return exceptions.server_error(detail=str(e))

@user_router.patch('/change-password', summary="Change user's password", status_code=200)
async def change_password(token: str, user: UserPasswordSchema, db: Session = Depends(get_db)):
    try:
        check_code = student_crud.change_password(db, token, user)
        db.commit()

        return success_response.success_message(detail="Password was successfully changed.")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)

    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
    
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
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))


@user_router.post('/resend-verification-link', summary="Resend Verification Link", status_code=200)
async def resend_email(user: ResendEmailSchema, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await user_crud.resend_link(db, user, backtask)
        db.commit()
        return success_response.success_message([], f"A link has been sent to {user.email_address}", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))

@user_router.post("/verify-email-token", summary="Verify Token from Email Verification Link.", status_code=200)
async def refresh_token(token: refreshTokenSchema, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await user_crud.verify_token(db, token.refresh_token, backtask)
        db.commit()
        return success_response.success_message([], f"Account has been successfully verified")
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@user_router.get('', summary="Get active user", status_code=200)
async def get_user(db: Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    try:
        user_detail = student_crud.get_user_detail(db, current_user)
        return success_response.success_message(user_detail)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail=e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@user_router.get('/mentors', summary="Get all mentors", status_code=200)
async def update_contact_info(language: str = Query(default=None), discipline: str = Query(default=None),
                              page: int= Query(default=None, ge=1), db:Session = Depends(get_db), 
                              page_size: int=10, current_user: dict = Depends(validate_active_client)):
    try:
        user_info = student_crud.get_mentors(db, current_user, language, discipline, page, page_size)
        return success_response.success_message(user_info, "", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
@user_router.post('/mentor-connect', summary="Connect with a mentor", status_code=200)
async def resend_email(details: UserConnectSchema, db: Session = Depends(get_db), 
                       current_user: dict = Depends(validate_active_client)):
    try:
        connection = student_crud.send_connection(db, current_user, details)
        db.commit()
        return success_response.success_message([], f"Connection request sent", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptions.unauthorized_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except ForbiddenException as e:
        return exceptions.forbidden_error(detail=e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))

@user_router.get('/search-universities', summary="Get all universities", status_code=200)
async def get_university(university: str = Query(default=None), location: str = Query(default=None),
                              course: str = Query(default=None), page: int= Query(default=None, ge=1), db:Session = Depends(get_db), 
                              page_size: int=10):
    try:
        user_info = student_crud.get_schools(db, university, location, course,  page, page_size)
        return success_response.success_message(user_info, "", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptsions.unauthorized_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
@user_router.get('/search-university/{school_slug}', summary="Get all universities", status_code=200)
async def get_university_details(school_slug: str, db:Session = Depends(get_db)):
    try:
        user_info = student_crud.get_school_details(db, school_slug)
        return success_response.success_message(user_info, "", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotAuthorizedException as e:
        return exceptsions.unauthorized_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))