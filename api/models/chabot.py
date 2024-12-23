from datetime import datetime
import enum
from sqlalchemy import TEXT, Column, Enum, Integer, String, ForeignKey,Text, DateTime, TIMESTAMP,JSON
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.schemas import SenderEnum, MessageStatusEnum


class ChatBot(Base):
    __tablename__ = 'chatbots'
    
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id'), nullable=False)
    sender = Column(Enum(SenderEnum), nullable=False)
    message = Column(TEXT, nullable=False)
    sent_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    status = Column(Enum(MessageStatusEnum), default=MessageStatusEnum.unread, nullable=False)
    
    session = relationship('Session', back_populates='chats')  



def query_similar_documents(query_text: str, collection, model, n_results=3):
    """Retrieve similar documents and generate a Gemini model prompt."""
    query_embedding = model.encode([query_text])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    if not results.get('documents'):
        raise ValueError("No similar documents found for the query.")

    similar_documents = results['documents']
    prompt = f"""
    You are a helpful assistant. Based on the following query and context, please provide the most relevant response.

    Query: {query_text}

    Context (Similar Documents):
    -----------------------------
    """
    for i, doc in enumerate(similar_documents, start=1):
        prompt += f"\nDocument {i}:\n{doc}\n"

    prompt += """
    Please generate a response based on the provided query and context. The response should be clear, concise, and relevant to the query.
    """
    return prompt




