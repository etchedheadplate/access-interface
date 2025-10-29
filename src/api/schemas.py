from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class LoginRequest(BaseModel):
    username: EmailStr
    password: str
