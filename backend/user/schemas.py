import datetime
from typing import Union
from pydantic import BaseModel, constr, EmailStr


class UpdateProfileData(BaseModel):
    name: str
    age: int
    program_level: constr(pattern=r'UG|PG')
    budget_min: int
    budget_max: int
    gender: constr(pattern=r'MALE|FEMALE|OTHER')