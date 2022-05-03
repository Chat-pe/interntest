from typing import Optional, Literal
from typing_extensions import TypedDict
from typing import (
    List
)
from datetime import date, datetime
import re

from pydantic import BaseModel, EmailStr, Field, validator


class Register(BaseModel):
    __tablename__ = "Register"
    phone: str
    signature: str
   
    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        schema_extra = {"examples": [{"phone": "+923331234567"}]}


class Verify(BaseModel):
    __tablename__ = "Verify"
    phone: str
    code: str
   
    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        schema_extra = {"examples": [{"phone": "+923331234567", "code": "123456"}]}