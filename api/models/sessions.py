from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey,Text, DateTime, TIMESTAMP,JSON, Enum
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from api.schemas import UserType, SessionStatusEnum


class Session(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user_type = Column(Enum(UserType), nullable=False)
    status = Column(Enum(SessionStatusEnum), default=SessionStatusEnum.active, nullable=False)
    started_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, default=func.now())

    user = relationship('NeovisChatbotUsers', back_populates='sessions')
    chats = relationship('ChatBot', back_populates='session')
    chat_transfers = relationship('ChatTransfer', back_populates='session')

    
