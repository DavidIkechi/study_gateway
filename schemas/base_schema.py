# Schemas
from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator, EmailStr, Field
from typing import List, Optional, Dict, Union, Any
from datetime import datetime
import re

class BaseModel(PydanticBaseModel):
    class config:
        orm_mode = True