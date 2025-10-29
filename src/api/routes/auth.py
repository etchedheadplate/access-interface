import httpx
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import EmailStr

from ..config import DB_BASE, Routes
from ..schemas import LoginRequest, RegisterRequest

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(username: EmailStr, password: str):
    request = RegisterRequest(email=username, password=password)
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + Routes.Open.Auth.REGISTER, json=request.model_dump())
        return response.json()


@router.post("/login")
async def login(username: EmailStr, password: str):
    request = LoginRequest(username=username, password=password)
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + Routes.Open.Auth.LOGIN, data=request.model_dump())
        return response.json()


@router.post("/check")
async def check(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.Auth.CHECK, headers=headers)
        return response.json()
