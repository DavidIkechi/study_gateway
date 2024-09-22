# Schemas
from .base_schema import BaseModel
from pydantic import EmailStr, validator, constr, Field
from datetime import datetime
from typing import Optional
import base64
import re

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
    profile: str = Field(..., pattern=r'^(?:data:image\/(jpeg|png|jpg);base64,)?[A-Za-z0-9+/]+={0,2}$')

    @validator('profile')
    def check_image_base64(cls, v):
        # Check for data URL scheme and strip it
        if v.startswith('data:image'):
            # This regex will strip the data URL scheme if present
            v = re.sub(r'^data:image\/(jpeg|png|jpg);base64,', '', v)

        # Ensure string is not empty after stripping
        if not v:
            raise ValueError('Base64 image data must not be empty')

        # Decode base64 string to binary data
        try:
            image_binary = base64.b64decode(v, validate=True)
        except Exception as e:
            raise ValueError('Invalid base64 image data')

        # Check the size of the decoded image (max 500KB)
        max_size = 500 * 1024  # 500 KB
        decoded_size = len(image_binary)
        if decoded_size > max_size:
            raise ValueError('Image size exceeds the 500KB limit')

        return v
    
class ConnectSchema(BaseModel):
    connect_ref: str
    status: bool
    
    @validator('status')
    def validate_status(cls, value):
        if not isinstance(value, bool):
            raise ValueError('Status must be a boolean value')
        return value
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
    
    @validator('birth_date', pre=True, always=True)
    def birth_date_must_be_in_past(cls, value):
        if value is None:
            return value
        
        # Ensure the value is parsed correctly as a datetime object if it's a string
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Birth date must be in the format YYYY-MM-DD')
        
        # Check if the date is in the future
        if value > datetime.now():
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
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
class ReasonSchema(BaseModel):
    email_address: EmailStr
    reason: Optional[str] = None
    
class StudentUpdateSchema(BaseModel):
    university: Optional[str] = None
    completed: Optional[bool] = None
    document_progress: Optional[float] = None
    visa_progress: Optional[float] = None
    course: Optional[str] = None
    degree: Optional[str] = None
    admission_progress: Optional[float] = None
    year: int = Field(..., ge=datetime.now().year)
    
    @validator('year')
    def validate_year(cls, value):
        current_year = datetime.now().year
        if value < current_year:
            raise ValueError(f'Year must be {current_year} or later')
        return value
    
    @validator('completed')
    def validate_status(cls, value):
        if not isinstance(value, bool):
            raise ValueError('Status must be a boolean value')
        return value