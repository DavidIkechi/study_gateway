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
from schemas.user_schema import UserSchema, CodeSchema, refreshTokenSchema, ResendEmailSchema
from fastapi.security import OAuth2PasswordRequestForm

from crud import waitlist_crud


waitlist_router = APIRouter(
    prefix="/waitlists",
    tags=["waitlists"]
)

@waitlist_router.post('', summary="Add waitlist", status_code=201)
async def create_waitlist(user: ResendEmailSchema, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await waitlist_crud.create_waitlist(db, user, backtask)
        db.commit()
        return success_response.success_message([], f"{user.email_address} successfully added to waitlist", 201)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
@waitlist_router.delete('/{email_address}', summary="Add waitlist", status_code=200)
async def delete_user(email_address: str, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await waitlist_crud.delete_waitlist(db, email_address, backtask)
        db.commit()
        return success_response.success_message([], f"{email_address} deleted succesfully from waitlist", 200)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
@waitlist_router.get('', summary="Get all waitlist", status_code=200)
async def get_waitlist(db: Session = Depends(get_db)):
    try:
        waited = waitlist_crud.get_all_waitlist(db)
        return waited  
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))