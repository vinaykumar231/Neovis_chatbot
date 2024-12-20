from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey,Text, DateTime, TIMESTAMP,JSON, Enum
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class UserType(str, enum.Enum):
    register = "register"
    internal = "internal"
    guest = "guest"

class SessionStatusEnum(enum.Enum):
    active = "active"
    closed = "closed"
    transferred = "transferred"

class Session(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(String(50), primary_key=True, index=True, nullable=False)
    user_id = Column(String(50), ForeignKey('users.user_id'), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    status = Column(Enum(SessionStatusEnum), default=SessionStatusEnum.active, nullable=False)
    started_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    ended_at = Column(TIMESTAMP, nullable=True)

    user = relationship('NeovisChatbotUsers', back_populates='sessions')
     
    chats = relationship('ChatBot', back_populates='session')  

    chat_transfers = relationship('ChatTransfer', back_populates='session')
