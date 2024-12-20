from datetime import datetime
from sqlalchemy import TEXT, Column, Integer, String, ForeignKey,Text, DateTime, TIMESTAMP,JSON
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


class ChatTransfer(Base):
    __tablename__ = 'chat_transfers'
    
    transfer_id = Column(String(50), primary_key=True, index=True, nullable=False)
    session_id = Column(String(50), ForeignKey('sessions.session_id'), nullable=False)
    transferred_by = Column(String(50), ForeignKey('users.user_id'), nullable=False)
    agent_id = Column(String(50), nullable=True)  
    transfer_reason = Column(TEXT, nullable=True)  
    transferred_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    resolved_at = Column(TIMESTAMP, nullable=True)  

    session = relationship('Session', back_populates='chat_transfers')

    transferred_by_user = relationship('User', back_populates='chat_transfers')

    agent = relationship('User', foreign_keys=[agent_id], back_populates='assigned_transfers')
