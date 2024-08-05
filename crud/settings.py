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

def country_states(db, country_slug):
    from db.main_model import StateModel
    get_country_id = check_country_by_slug(db, country_slug).id

    states = StateModel.get_state_by_country(db, get_country_id).options(
        load_only('name','slug')).order_by(StateModel.name).all()

    return states

def check_states_by_slug(db, slug):
    from db.main_model import StateModel
    get_state = StateModel.get_state_by_slug(db, slug)
    
    if not get_state:
        raise NotFoundException(f"State with id: {slug} not found")

    return get_state

def country_codes(db):
    from db.main_model import CountryCodeModel

    return CountryCodeModel.get_all_countries(db).options(
        load_only('country_name','slug','phone_code','iso3')).order_by(CountryCodeModel.country_name).all()
    
def degrees(db):
    from db.main_model import DegreeModel

    return DegreeModel.get_all_degrees(db).options(
        load_only('degree_name','slug')).order_by(DegreeModel.degree_name).all()

def check_degree_by_slug(db, slug):
    from db.main_model import DegreeModel
    get_degree = DegreeModel.get_degree_by_slug(db, slug)
    
    if not get_degree:
        raise NotFoundException(f"Degree with id: {slug} not found")

    return get_degree
 
def degree_soughts(db):
    from db.main_model import DegreeSoughtModel

    return DegreeSoughtModel.get_all_degrees(db).options(
        load_only('degree_name','slug')).order_by(DegreeSoughtModel.degree_name).all()

def check_sought_by_slug(db, slug):
    from db.main_model import DegreeSoughtModel
    get_sought = DegreeSoughtModel.get_degree_by_slug(db, slug)
    
    if not get_sought:
        raise NotFoundException(f"Degree Sought with id: {slug} not found")

    return get_sought

def courses(db):
    from db.main_model import CourseModel

    return CourseModel.get_all_courses(db).options(
        load_only('course_name','slug')).order_by(CourseModel.course_name).all()
    
def check_courses_by_slug(db, slug):
    from db.main_model import CourseModel
    get_course = CourseModel.get_course_by_slug(db, slug)
    
    if not get_course:
        raise NotFoundException(f"Course with id: {slug} not found")

    return get_course

def packages(db):
    from db.main_model import PackageModel

    return PackageModel.get_all_packages(db).options(
        load_only('package_name','slug')).order_by(PackageModel.package_name).all()
    
def check_packages_by_slug(db, slug):
    from db.main_model import PackageModel
    get_package = PackageModel.get_package_by_slug(db, slug)
    
    if not get_package:
        raise NotFoundException(f"Package with id: {slug} not found")

    return get_package

def pricing(db):
    from db.main_model import PricingModel

    return PricingModel.get_all_pricings(db).options(
        load_only('name','slug','price','requirement','description','benefits')).all()
    
def check_pricing_by_slug(db, slug):
    from db.main_model import PricingModel
    get_price = PricingModel.get_pricing_by_slug(db, slug)
    
    if not get_price:
        raise NotFoundException(f"Price with id: {slug} not found")

    return get_price

def get_package_pricing(db, slug):
    from db.main_model import PricingModel
    package_id = check_packages_by_slug(db, slug).id

    return PricingModel.get_pricing_by_package(db, package_id).options(
        load_only('name','slug','price','requirement','description','benefits')).all()
    
def check_language_by_slug(db, slug):
    from db.main_model import LanguageModel
    get_language = LanguageModel.get_pricing_by_slug(db, slug)
    
    if not get_language:
        raise NotFoundException(f"Language with id: {slug} not found")

    return get_price

def get_languages(db, slug):
    from db.main_model import LanguageModel

    return LanguageModel.get_all_languages(db).options(
        load_only('name','slug')).all()
