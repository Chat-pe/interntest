from optparse import Option
from time import time
from typing import Optional, Literal
from typing_extensions import TypedDict
from typing import (
    List
)
from datetime import date, datetime
import re,uuid

from api.database import pdb
 
from pydantic import BaseModel, EmailStr, Field, validator

from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")



class User(BaseModel):
    __tablename__ = "Users"
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    phone: str
    name: str = Field(..., min_length=3, max_length=50)
    date_joined: Optional[date] = datetime.date(datetime.now())


    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",

            }
        }





class Phone(BaseModel):

    phone: str = Field(...)

    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v