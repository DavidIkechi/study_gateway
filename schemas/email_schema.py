from .base_schema import BaseModel
from pydantic import EmailStr, validator
from typing import List, Dict, Any

class EmailSchema(BaseModel):
    body: Dict[str, Any]