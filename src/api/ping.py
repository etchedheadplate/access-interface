import httpx
from dotenv import load_dotenv
from fastapi import APIRouter

from src.api.config import DB_BASE, Routes

load_dotenv()

router = APIRouter(tags=["Ping"])


@router.get("/ping")
async def ping_database():
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + Routes.Open.PING)
        return {"from_database_service": response.json()}
