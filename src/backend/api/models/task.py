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



class Task(BaseModel):
    __tablename__ = "Task"
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=3, max_length=50)
    phone: str

    uniquelink: Optional[str] = None
    details: Optional[str] = None
    expiry_date: Optional[str] = None
    category: Optional[Literal["work", "personal"]] = "personal"
    status: Optional[Literal["active", "inactive", "completed"]] = "active"
    date_created: Optional[str] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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





class UpdateTask(BaseModel):
    __tablename__ = "Task"
    uniquelink: str
    status: Literal["active", "inactive", "completed"]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "uniquelink": "5e9f9b0b7c8d1a0e8b8b8b8b",
                "status": "active",

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


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "phone": "+2348012345678",

            }
        }