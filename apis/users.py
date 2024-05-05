from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db 
# from auth import validate_active_client
from response_handler import error_response as exceptions
from response_handler import success_response
from exceptions import BadExceptions, NotFoundException, ServerErrorException
from schemas.user_schema import UserSchema
from crud import user_crud


user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post('', summary="Create a new user", status_code=201)
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    try:
        create_user = user_crud.create_user(db, user)
        db.commit()
        return success_response.created([], f"User {user.email_address} created successfully.", 201)
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
        
    except Exception as e:
        return exceptions.server_error(str(e))

@user_router.post('/login', summary="Login a user", status_code=200)
async def login_user():
    pass