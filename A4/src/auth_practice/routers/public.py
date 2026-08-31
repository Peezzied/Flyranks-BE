from fastapi import APIRouter

router = APIRouter(prefix="/public")

@router.get("/info")
def info():
    return { "message": "Welcome stranger! This info is public." }

