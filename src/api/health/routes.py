import httpx
from dotenv import load_dotenv
from fastapi import APIRouter

from src.api.config import DB_BASE, DBRoutes

load_dotenv()

router_health = APIRouter(tags=["health"])


@router_health.get("/ping_db")
async def send_ping():
    async with httpx.AsyncClient() as client:
        response = await client.post(DB_BASE + DBRoutes.HEALTH_PING)
        return {"from_database_service": response.json()}
