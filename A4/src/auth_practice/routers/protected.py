import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth_practice.supabase import supabase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/protected")

security = HTTPBearer()

def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        user = supabase.auth.get_user(credentials.credentials).user
        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})

@router.get("/profile")
def profile(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user

@router.get("/dashboard")
def profile(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user
