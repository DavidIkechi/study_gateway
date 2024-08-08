# Schemas
from .base_schema import BaseModel
from pydantic import EmailStr, validator, constr, Field
from datetime import datetime
from typing import Optional
import base64

class UserConnectSchema(BaseModel):
    mentor_email_address: EmailStr
    university: str
    year: int = Field(..., ge=datetime.now().year)  # Ensure year is from current year onwards

    @validator('year')
    def validate_year(cls, value):
        current_year = datetime.now().year
        if value < current_year:
            raise ValueError(f'Year must be {current_year} or later')
        return value
        
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
class ChangeProfileImageSchema(BaseModel):
    profile: str = Field(..., pattern=r'^[A-Za-z0-9+/]+={0,2}$')  # Ensures base64 format

    @validator('profile')
    def check_image_base64(cls, v):
        # Strip whitespace and check for empty string
        v = v.strip()
        if not v:
            raise ValueError('Base64 image data must not be empty')

        # Check for valid image formats
        if not (v.startswith('/9j/') or v.startswith('iVBORw0KGgo')):
            raise ValueError('Image must be in JPEG, JPG, or PNG format')

        # Decode base64 string to binary data
        try:
            image_binary = base64.b64decode(v)
        except Exception as e:
            raise ValueError('Invalid base64 image data')

        # Check the size of the decoded image (max 500KB)
        max_size = 500 * 1024  # 500 KB
        decoded_size = len(image_binary)
        if decoded_size > max_size:
            raise ValueError('Image size exceeds the 500KB limit')

        return v
    
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
    
    
    