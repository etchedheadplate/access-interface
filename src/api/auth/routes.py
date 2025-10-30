import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Form, HTTPException
from pydantic import EmailStr

from src.api.config import DB_BASE, Routes

from .schemas import LoginRequest, RegisterRequest

load_dotenv()

router = APIRouter(tags=["Auth"])


@router.post("/register")
async def register(username: EmailStr, password: str):
    request = RegisterRequest(email=username, password=password)
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + Routes.Open.Auth.REGISTER, json=request.model_dump())
        return response.json()


@router.post("/login")
async def login(username: EmailStr = Form(...), password: str = Form(...)):
    request = LoginRequest(username=username, password=password)
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + Routes.Open.Auth.LOGIN, data=request.model_dump())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
