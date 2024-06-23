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

from crud import subscriber_crud


subscriber_router = APIRouter(
    prefix="/subscribers",
    tags=["Subscribers"]
)

@subscriber_router.post('', summary="Add Subscriber", status_code=201)
async def create_subscriber(user: ResendEmailSchema, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await subscriber_crud.create_subscriber(db, user, backtask)
        db.commit()
        return success_response.success_message([], f"{user.email_address} subscribed successfully", 201)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
@subscriber_router.delete('/{email_address}', summary="Add Subscriber", status_code=200)
async def delete_user(email_address: str, backtask: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        await subscriber_crud.delete_subscriber(db, email_address, backtask)
        db.commit()
        return success_response.success_message([], f"{email_address} deleted succesfully", 201)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))