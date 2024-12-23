import os
from dotenv import load_dotenv
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import google.generativeai as genai
from database import get_db
from ..schemas import QueryRequest, IDValidationRequest
from chroma_Vector_db.chroma import collection, model, client
from ..models.chabot import query_similar_documents
from auth.auth_bearer import JWTBearer, get_current_user


load_dotenv()
router = APIRouter()


api_key = os.getenv("API_KEY_gm")

genai.configure(api_key=api_key)

system_prompt = """ Persona: You are a helpful assistant. Based on the following query and context, please provide the most relevant response.
Task: Answer all questions about services and related information. Provide detailed and kind responses in a conversational manner.
"""

@router.post("/chatbot_response/", dependencies=[Depends(JWTBearer()), Depends(get_current_user)])
async def query_documents(data: QueryRequest, db: Session = Depends(get_db)):
    try:
        query_text = data.query
        prompt = query_similar_documents(query_text, collection, model, n_results=3)

        gemini_model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",
            system_instruction=system_prompt
        )
        
        contextual_response = gemini_model.generate_content(prompt)
        
        if hasattr(contextual_response, 'content'):  
            contextual_response = contextual_response.content  
        
        if not isinstance(contextual_response, str):
            contextual_response = str(contextual_response.text)
        
        return {"response": contextual_response}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")
 
