import logging
from fastapi import APIRouter, Depends, Request, HTTPException

from auth_practice.supabase import supabase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/protected")

@router.get("/profile")
def profile(req: Request, BEARER="Bearer "):
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
        raise HTTPException(status_code=401, detail={ "error": "Invalid or expired token" })
