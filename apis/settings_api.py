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

@settings_router.get('/countries', summary="Get all countries", status_code=200)
async def get_country(db: Session = Depends(get_db)):
    from crud.settings import get_countries
    try:
        return success_response.success_message(get_countries(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))

@settings_router.get('/nationalities', summary="Get all Nationalities", status_code=200)
async def get_nationality(db: Session = Depends(get_db)):
    from crud.settings import get_nationalities
    try:
        return success_response.success_message(get_nationalities(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))

@settings_router.get('/cities/{country_slug}', summary="Get all cities in a country", status_code=200)
async def get_cities(country_slug: str, db: Session = Depends(get_db)):
    from crud.settings import country_cities
    try:
        return success_response.success_message(country_cities(db, country_slug))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
    
@settings_router.get('/gender', summary="Get all Genders", status_code=200)
async def get_genders(db: Session = Depends(get_db)):
    from crud.settings import get_gender
    try:
        return success_response.success_message(get_gender(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))