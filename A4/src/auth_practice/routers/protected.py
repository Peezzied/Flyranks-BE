import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request

from auth_practice.supabase import supabase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/protected")

def get_current_user(req: Request, BEARER = "Bearer "):
    auth_header = req.headers.get("authorization")

    if not auth_header or not auth_header.startswith(BEARER):
        raise HTTPException(status_code=401, detail={"error": "Access token required."})
    
    token = auth_header[len(BEARER):]
    
    try:
        user = supabase.auth.get_user(token).user
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
