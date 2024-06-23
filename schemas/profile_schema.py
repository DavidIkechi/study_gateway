from .base_schema import BaseModel
from pydantic import EmailStr, validator
from datetime import datetime
from typing import Optional

class UserInfoSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[datetime] = None
    nationality: Optional[str] = None  # Assuming you want to add email as well

    @validator('first_name')
    def first(cls, value):
        if value is not None:
            return value.title()
    
    @validator('last_name')
    def last(cls, value):
        if value is not None:
            return value.title()

    @validator('birth_date')
    def birth_date_must_be_in_past(cls, value):
        if value and value > datetime.now():
            raise ValueError('Birth date must be in the past')
        return value
    
class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str  
    
class ContactInfoSchema(BaseModel):
    email_address: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address2: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    zip_code: Optional[str] = None
    
class DegreeSchema(BaseModel):
    degree: Optional[str] = None
    degree_sought: Optional[str] = None
    courses: Optional[str] = None
    course_extra: Optional[str] = None
    highest_degree_extra: Optional[str] = None
    
class ExtraSchema(BaseModel):
    course_extra: Optional[str] = None
    highest_degree_extra: Optional[str] = None
    email_address2: Optional[str] = None
    address2: Optional[str] = None


    