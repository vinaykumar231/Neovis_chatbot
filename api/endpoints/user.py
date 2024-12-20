from datetime import datetime, timedelta
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


@router.post('/NeovisChatbotUserss/login/')
async def NeovisChatbotUserss(credential: LoginInput):
    try:
        response = user_ops.NeovisChatbotUserss_login(credential)
        return response
    except HTTPException as e:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=f"login failed: {str(e)}")


@router.post("/insert/neovis_chatbot_register/")
def NeovisChatbotUsers_register(data: UserCreate, db: Session = Depends(get_db)):
    try:
        if not NeovisChatbotUsers.validate_email(data.user_email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        if not NeovisChatbotUsers.validate_password(data.user_password):
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

        if not NeovisChatbotUsers.validate_phone_number(data.phone_no):
            raise HTTPException(status_code=400, detail="Invalid phone number")

        utc_now = pytz.utc.localize(datetime.utcnow())
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

        hashed_password = bcrypt.hashpw(data.user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        usr = NeovisChatbotUsers(
            user_name=data.user_name,
            user_email=data.user_email,
            user_password=hashed_password,
            user_type=UserType.guest,  
            phone_no=data.phone_no,
            created_on=ist_now,
            updated_on=ist_now
        )
        db.add(usr)
        db.commit()  

        response = api_response(200, message="User Created successfully")
        return response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"filed to hr Register")


@router.get("/get_all_users/", dependencies=[Depends(JWTBearer()), Depends(get_internal)])
def get_current_user_details( db: Session = Depends(get_db)):
    try:
        all_user=[]
        user_db=db.query(NeovisChatbotUsers).all()
        for user in user_db:
            user_details = {
                "user_id": user.user_id,
                "username": user.user_name,
                "email": user.user_email,
                "user_type": user.user_type,
                "phone_no" : user.phone_no,

            }
            all_user.append(user_details)
        return all_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

@router.get("/get_my_profile")
def get_current_user_details(current_user: NeovisChatbotUsers = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_details = {
            # "user_id": current_user.user_id,
            "username": current_user.user_name,
            "email": current_user.user_email,
            "user_type": current_user.user_type,
            "phone_no" : current_user.phone_no,

        }
        return api_response(data=user_details, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    


@router.put("/update_user_type/")
async def update_user_type(update: UserTypeUpdateNovis, db: Session = Depends(get_db)):

    user = db.query(NeovisChatbotUsers).filter(NeovisChatbotUsers.user_id == update.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.user_type = update.user_type
    db.commit()
    return {"message": "User type updated successfully"}

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(NeovisChatbotUsers).filter(NeovisChatbotUsers.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}

