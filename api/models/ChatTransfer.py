from datetime import datetime
from sqlalchemy import TEXT, Column, Integer, String, ForeignKey,Text, DateTime, TIMESTAMP,JSON
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class ChatTransfer(Base):
    __tablename__ = 'chat_transfers'
    
    transfer_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id'))
    transferred_by = Column(Integer, ForeignKey('users.user_id'))
    transfer_reason = Column(TEXT, nullable=True)  
    transferred_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    resolved_at = Column(TIMESTAMP, nullable=True)  

    session = relationship('Session', back_populates='chat_transfers')
    transferred_by_user = relationship('NeovisChatbotUsers', back_populates='chat_transfers')

    

