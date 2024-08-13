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
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/states/{country_slug}', summary="Get all states in a country", status_code=200)
async def get_cities(country_slug: str, db: Session = Depends(get_db)):
    from crud.settings import country_states
    try:
        return success_response.success_message(country_states(db, country_slug))
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/gender', summary="Get all Genders", status_code=200)
async def get_genders(db: Session = Depends(get_db)):
    from crud.settings import get_gender
    try:
        return success_response.success_message(get_gender(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
    
@settings_router.get('/country-code', summary="Get all countries code", status_code=200)
async def get_country(db: Session = Depends(get_db)):
    from crud.settings import country_codes
    try:
        return success_response.success_message(country_codes(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/degree-sought', summary="Get all degree sought", status_code=200)
async def get_country(db: Session = Depends(get_db)):
    from crud.settings import degree_soughts
    try:
        return success_response.success_message(degree_soughts(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/degrees', summary="Get all degrees", status_code=200)
async def get_degrees(db: Session = Depends(get_db)):
    from crud.settings import degrees
    try:
        return success_response.success_message(degrees(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/courses', summary="Get all courses", status_code=200)
async def get_country(db: Session = Depends(get_db)):
    from crud.settings import courses
    try:
        return success_response.success_message(courses(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/packages', summary="Get all packages", status_code=200)
async def get_packages(db: Session = Depends(get_db)):
    from crud.settings import packages
    try:
        return success_response.success_message(packages(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))

        
@settings_router.get('/package-prices/{package_slug}', summary="Get all Prices for package", status_code=200)
async def get_country(package_slug: str, db: Session = Depends(get_db)):
    from crud.settings import get_package_pricing
    try:
        return success_response.success_message(get_package_pricing(db, package_slug))
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))

@settings_router.get('/languages', summary="Get all languages", status_code=200)
async def get_languag(db: Session = Depends(get_db)):
    from crud.settings import get_languages
    try:
        return success_response.success_message(get_languages(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))

        
@settings_router.get('/languages/{language_slug}', summary="Get single language", status_code=200)
async def get_language(language_slug: str, db: Session = Depends(get_db)):
    from crud.settings import check_language_by_slug
    try:
        return success_response.success_message(check_language_by_slug(db, language_slug))
    
    except BadExceptions as e:
        return exceptions.bad_request_error(detail = e.detail)
    
    except NotFoundException as e:
        return exceptions.not_found_error(detail = e.detail)
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/universities', summary="Get all Universities", status_code=200)
async def get_uni(db: Session = Depends(get_db)):
    from crud.settings import get_universities
    try:
        return success_response.success_message(get_universities(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))

        
@settings_router.get('/universities/{uni_slug}', summary="Get university", status_code=200)
async def get_single_uni(uni_slug: str, db: Session = Depends(get_db)):
    from crud.settings import check_university_by_slug
    try:
        return success_response.success_message(check_university_by_slug(db, uni_slug))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
@settings_router.get('/school-locations', summary="Get all locations for school", status_code=200)
async def get_uni(db: Session = Depends(get_db)):
    from crud.settings import get_state_universities
    try:
        return success_response.success_message(get_state_universities(db))
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
