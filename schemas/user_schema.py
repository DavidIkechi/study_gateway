# Schemas
from .base_schema import BaseModel
from pydantic import EmailStr, validator
        
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
    
    
    