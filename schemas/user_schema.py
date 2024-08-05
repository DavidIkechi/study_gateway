# Schemas
from .base_schema import BaseModel
from pydantic import EmailStr, validator
from datetime import datetime
from typing import Optional
        
class UserSchema(BaseModel):
    email_address: EmailStr
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    
    @validator('password')
    def check_passwords(cls, v):
        return v.strip()
    
    @validator('first_name')
    def check_first_name(cls, v):
        return v.title()
    
    @validator('last_name')
    def check_last_name(cls, v):
        return v.title()
    
    @validator('confirm_password')
    def check_confirm_passwords(cls, v):
        return v.strip()
    
class MentorSchema(BaseModel):
    email_address: EmailStr
    password: str
    first_name: str
    last_name: str
    language: str
    course: str
    degree: str
    nationality: str
    gender: str
    birth_date: Optional[datetime] = None

    
    @validator('password')
    def check_passwords(cls, v):
        return v.strip()
    
    @validator('first_name')
    def check_first_name(cls, v):
        return v.title()
    
    @validator('last_name')
    def check_last_name(cls, v):
        return v.title()
    
    @validator('birth_date')
    def birth_date_must_be_in_past(cls, value):
        if value and value > datetime.now():
            raise ValueError('Birth date must be in the past')
        return value
    
class UserPasswordSchema(BaseModel):
    password: str
    confirm_password: str
    
    @validator('password')
    def check_passwords(cls, v):
        return v.strip()
    
    @validator('confirm_password')
    def check_confirm_passwords(cls, v):
        return v.strip()
    
class CodeSchema(BaseModel):
    email_address: EmailStr
    otp: str

class refreshTokenSchema(BaseModel):
    refresh_token: str
    
class ResendEmailSchema(BaseModel):
    email_address: EmailStr
    
class NameSchema(BaseModel):
    first_name: str = None
    last_name: str = None
    
    
    