import base64
from typing import Any
from uuid import uuid4

import httpx

from api.config import DB_BASE


async def generate_id() -> str:
    uid = uuid4()
    id = base64.urlsafe_b64encode(uid.bytes).rstrip(b"=").decode("ascii")
    return id


async def call_route(route: str, params: dict[str, Any] | None = None, token: str | None = None) -> dict[str, Any]:
    url = DB_BASE + route
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
