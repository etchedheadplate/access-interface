from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr

from src.api.dependancies import get_user_client
from src.api.schemas import LoginRequest, RegisterRequest
from src.services.clients import UserClient

router = APIRouter(tags=["Auth"])


@router.post("/register")
async def register(
    username: EmailStr = Form(...), password: str = Form(...), client: UserClient = Depends(get_user_client)
):
    request = RegisterRequest(email=username, password=password)
    return await client.register(request)


@router.post("/login", include_in_schema=False)
async def login(
    username: EmailStr = Form(...), password: str = Form(...), client: UserClient = Depends(get_user_client)
):
    request = LoginRequest(username=username, password=password)
    return await client.login(request)
