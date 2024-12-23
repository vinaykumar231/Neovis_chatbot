from datetime import datetime, timedelta
import httpx
import jwt
from fastapi import APIRouter, Depends, HTTPException,Form
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from auth.auth_bearer import JWTBearer, get_current_user, get_guest, get_internal, get_register, get_guest_or_register
from database import get_db, api_response
from ..models.user import NeovisChatbotUsers
from ..schemas import LoginInput, ChangePassword, UserCreate, UpdateUser, UserType,UserTypeUpdateNovis
import bcrypt
import pytz
from sqlalchemy.orm import joinedload

router = APIRouter()

user_ops = NeovisChatbotUsers()


BASE_URL = "https://shark-app-6wiyn.ondigitalocean.app/api/v1"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"
TASK_ENDPOINT = f"{BASE_URL}/tasks/{{id}}"
LOGIN_PAYLOAD = {"email": "newAI@gmail.com", "password": "@test#123"}


async def fetch_task_by_id(task_id: int, email: str, password: str, db: Session) -> dict:
    async with httpx.AsyncClient() as client:
        login_payload = {"email": email, "password": password}
        login_response = await client.post(LOGIN_ENDPOINT, json=login_payload)
        
        if login_response.status_code != 201:
            print(f"Login failed: {login_response.status_code} {login_response.text}")
            raise ValueError("Unable to log in.")

        data = login_response.json()
        token = data.get("token")
        user_id = data["user"]["id"]
        user_role = data["user"]["user_role"]["role"]

        if not token:
            raise ValueError("Token not found in login response.")

        user_db = NeovisChatbotUsers(
            Task_id=task_id,
            user_email=email,
            user_type=user_role
        )
        db.add(user_db)
        db.commit()

        data= {
            f"message": "login Sucessfully",
            "user_email":email,
            "user_id": user_id,
            "user_role": user_role,
            "user_role": user_role,
            "token": token

        }

        return data

@router.post('/NeovisChatbotUserss/login/')
async def NeovisChatbotUserss(task_id: int, login_input: LoginInput, db: Session = Depends(get_db)):
    try:
        response = await fetch_task_by_id(task_id=task_id, email=login_input.email, password=login_input.password, db=db)

        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Login failed: {str(e)}")



