from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db 
# from auth import validate_active_client
from response_handler import error_response as exceptions
from response_handler import success_response
from exceptions import BadExceptions, NotFoundException, ServerErrorException


settings_router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)

@settings_router.get('/disciplines', summary="Get all disciplines", status_code=200)
async def get_settings_frequencies(db: Session = Depends(get_db)):
    from crud.settings import get_all_discipline
    try:
        return success_response.success_message(get_all_discipline(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))