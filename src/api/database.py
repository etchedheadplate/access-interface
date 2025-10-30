from uuid import UUID

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.api.auth import oauth2_scheme
from src.api.config import DB_BASE, Routes

load_dotenv()

router = APIRouter(prefix="/database", tags=["Database"])


@router.get("/users")
async def get_users(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.USERS, headers=headers)
        return response.json()


@router.get("/users/{id}")
async def get_user(id: UUID, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.USERS + str(id), headers=headers)
        return response.json()


@router.get("/groups")
async def get_groups(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.GROUPS, headers=headers)
        return response.json()


@router.get("/groups/{id}")
async def get_group(id: PositiveInt, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.GROUPS + str(id), headers=headers)
        return response.json()


@router.get("/permissions")
async def get_permissions(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.PERMISSIONS, headers=headers)
        return response.json()


@router.get("/permissions/{id}")
async def get_permission(id: PositiveInt, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.PERMISSIONS + str(id), headers=headers)
        return response.json()


@router.get("/resources")
async def get_resources(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.RESOURCES, headers=headers)
        return response.json()


@router.get("/resources/{id}")
async def get_resource(id: PositiveInt, token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_BASE + Routes.Open.DB.RESOURCES + str(id), headers=headers)
        return response.json()
