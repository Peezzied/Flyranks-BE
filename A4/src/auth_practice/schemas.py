from pydantic import BaseModel, EmailStr, Field

class UserAuth(BaseModel):
    email: EmailStr 
    password: str