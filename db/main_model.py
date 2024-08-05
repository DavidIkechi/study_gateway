from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text

from .discipline_model import DisciplineModel
from .user_model import UserModel
from .country_model import CountryModel
from .nationality_model import NationalityModel
from .gender_model import GenderModel
from .cities_model import CityModel
from .subscribers_model import SubscriberModel
from .states_model import StateModel
from .country_code_model import CountryCodeModel
from .courses import CourseModel
from .profile_model import ProfileModel
from .degree_sought import DegreeSoughtModel
from .degree import DegreeModel
from .additional_profile import AdditionalUserDetails
from .package_model import PackageModel
from .pricing_model import PricingModel
from .waitlist_model import WaitlistModel
from .language_model import LanguageModel
from .addtional_mentor import AdditionalMentors
 
import sys
sys.path.append("..")

# Client Table.
class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)    
    
    # get the client object
    @staticmethod
    def get_client_object(db: Session):
        return db.query(Client)
                              
    # get the client by ID
    @staticmethod
    def get_client_by_id(db: Session, id: int):
        return Client.get_client_object(db).get(id)
    
    @staticmethod
    def create_single_client(client_data: dict):
        return Client(**client_data)  
    
    @staticmethod
    def retrieve_all_client(db: Session):
        return Client.get_client_object(db).options(load_only(Client.slug, Client.status)).all()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    # static method
    @staticmethod
    def update_single_client(db: Session, client_id, client_data): 
        client = Client.get_client_by_id(db, client_id)
        for key, value in client_data.items():
            setattr(client, key, value)
        return client
           
