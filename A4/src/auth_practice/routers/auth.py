from fastapi import APIRouter, HTTPException, status
import logging

from auth_practice.supabase import supabase
from auth_practice.schemas import UserAuth

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: UserAuth):
    try:
        response = supabase.auth.sign_up(
            {
                "email": user_data.email,
                "password": user_data.password,
            }
        )
        
        return response.user
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail="Bad Request")

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_data: UserAuth):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": user_data.email,
                "password": user_data.password,
            }
        )
    
        return response.session
    except:
        raise HTTPException(status_code=400, detail="Bad Request")