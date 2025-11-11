from urllib.parse import urljoin

import httpx
from fastapi import APIRouter

from src.config import Settings

router = APIRouter(tags=["Ping"])
settings = Settings()  # type: ignore[call-arg]


@router.get("/ping")
async def ping_database():
    async with httpx.AsyncClient() as client:
        response = await client.post(urljoin(settings.DB_SERVICE_BASE_URL, "/ping"))
        return response.json()
