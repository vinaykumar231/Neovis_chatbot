from pydantic import BaseModel,  Field, EmailStr, validator
from typing import Optional, List
from fastapi import UploadFile, File
from datetime import date, datetime
from enum import Enum
from sqlalchemy import JSON
import re


######################################## User logiin and register #############################
class LoginInput(BaseModel):
    Task_id:int
    email: str
    user_password: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str

    class Config:
        from_attributes = True


class UserType(str, Enum):
    register = "register"
    internal = "internal"
    guest = "guest"
    
   


class UserCreate(BaseModel):
    user_name: str
    user_email: str
    user_password: str
    user_type: UserType = UserType.guest
    phone_no: str

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    phone_no: Optional[int] = None
    user_type: Optional[str] = None
    current_password: Optional[str] = None

class UserTypeUpdateNovis(BaseModel):
    user_id: int
    user_type: str

##################################################  for chat ###################################################
class QueryRequest(BaseModel):
    query: str

class IDValidationRequest(BaseModel):
    id: str
