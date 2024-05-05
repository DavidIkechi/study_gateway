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