from fastapi import APIRouter, Depends, Request, HTTPException

router = APIRouter(prefix="/protected")

@router.get("/profile")
def profile(req: Request, BEARER="Bearer "):
    auth_header = req.headers.get("authorization")

    if not auth_header or not auth_header.startswith(BEARER):
        raise HTTPException(status_code=401, detail={"error": "Access token required."})
    
    token = auth_header[len(BEARER):]
