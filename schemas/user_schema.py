# Schemas
from .base_schema import BaseModel
from pydantic import EmailStr, validator
        
class UserSchema(BaseModel):
    email_address: EmailStr
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
    
    
    