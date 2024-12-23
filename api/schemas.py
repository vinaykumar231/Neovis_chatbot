from pydantic import BaseModel,  Field, EmailStr, validator
from typing import Optional, List
from fastapi import UploadFile, File
from datetime import date, datetime
from enum import Enum
from sqlalchemy import JSON
import re
import enum


######################################## User logiin and register #############################
class LoginInput(BaseModel):
    email: str
    password: str


##################################### for session #######################################################

class UserType(str, enum.Enum):
    register = "register"
    internal = "internal"
    guest = "guest"

class SessionStatusEnum(enum.Enum):
    active = "active"
    closed = "closed"
    transferred = "transferred"

##################################################  for chat ###################################################


class SenderEnum(enum.Enum):
    user = "user"
    bot = "bot"
    agent = "agent"

class MessageStatusEnum(enum.Enum):
    unread = "unread"
    read = "read"
class QueryRequest(BaseModel):
    query: str

class IDValidationRequest(BaseModel):
    id: str

