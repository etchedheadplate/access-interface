import httpx
from dotenv import load_dotenv
from fastapi import APIRouter

from ..config import DB_BASE, Routes

load_dotenv()

router = APIRouter(tags=["Health"])


@router.get("/ping_db")
async def send_ping():
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + Routes.Open.PING)
        return {"from_database_service": response.json()}
