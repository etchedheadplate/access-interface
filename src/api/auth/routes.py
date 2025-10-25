import httpx
from dotenv import load_dotenv
from fastapi import APIRouter

from src.api.auth.schemas import CheckRequest, LoginRequest, RegisterRequest
from src.api.config import DB_BASE, DBRoutes

load_dotenv()

router_auth = APIRouter(prefix="/auth", tags=["auth"])


@router_auth.post("/register")
async def register(request: RegisterRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + DBRoutes.AUTH_REGISTER, json=request.model_dump())
        return response.json()


@router_auth.post("/login")
async def login(request: LoginRequest):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + DBRoutes.AUTH_LOGIN, data=request.model_dump(), headers=headers)
        return response.json()


@router_auth.post("/check")
async def check(request: CheckRequest):
    headers = {"Authorization": f"Bearer {request.token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + DBRoutes.AUTH_CHECK, headers=headers)
        return response.json()
