import sys
sys.path.append("..")
from utils import *
from db.session import Session
from sqlalchemy.orm import Session, load_only, relationship
from exceptions import BadExceptions, NotFoundException, ServerErrorException, NotAuthorizedException

def get_all_discipline(db):
    from db.main_model import DisciplineModel
    all_disciplines = DisciplineModel.get_all_disciplines(db).options(
            load_only('discipline_name', 'slug', 'icons')).all()
    
    return all_disciplines

def check_disciplines_by_slug(db, slug):
    from db.main_model import DisciplineModel
    get_discipline = DisciplineModel.get_discipline_by_slug(db, slug)
    
    if not get_discipline:
        raise NotFoundException(f"Discipline with id: {slug} not found")

    return get_discipline

def get_countries(db):
    from db.main_model import CountryModel

    return CountryModel.get_all_countries(db).options(
        load_only('country_name','slug')).order_by(CountryModel.country_name).all()

def get_nationalities(db):
    from db.main_model import NationalityModel
    
    return NationalityModel.get_all_nationalities(db).options(
        load_only('nationality','slug')).order_by(NationalityModel.nationality).all()

def get_gender(db):
    from db.main_model import GenderModel

    return GenderModel.get_all_gender(db).options(
        load_only('name','slug')).all()

def check_gender_by_slug(db, slug):
    from db.main_model import GenderModel
    get_gender =GenderModel.check_gender_slug(db, slug)
    
    if not get_gender:
        raise NotFoundException(f"Gender with id: {slug} not found")

    return get_gender

def check_country_by_slug(db, slug):
    from db.main_model import CountryModel
    get_country = CountryModel.get_country_by_slug(db, slug)
    
    if not get_country:
        raise NotFoundException(f"Country with id: {slug} not found")

    return get_country

def check_country_by_name(db, name):
    from db.main_model import CountryModel
    get_country = CountryModel.get_country_by_name(db, name)
    
    if not get_country:
        raise NotFoundException(f"Country: {name} not found")

    return get_country

def check_nationality_by_slug(db, slug):
    from db.main_model import NationalityModel
    get_nationality = NationalityModel.get_nationality_by_slug(db, slug)
    
    if not get_nationality:
        raise NotFoundException(f"Nationality with id: {slug} not found")

    return get_nationality

def check_cities_by_slug(db, slug):
    from db.main_model import CityModel
    get_city = CityModel.get_city_by_slug(db, slug)
    
    if not get_city:
        raise NotFoundException(f"City with id: {slug} not found")

    return get_city

def country_cities(db, country_slug):
    from db.main_model import CityModel
    get_country_id = check_country_by_slug(db, country_slug).id

    cities = CityModel.get_city_by_country(db, get_country_id).options(
        load_only('name','slug')).order_by(CityModel.name).all()

    return cities