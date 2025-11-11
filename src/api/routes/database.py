from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.api.dependancies import (
    get_group_client,
    get_permission_client,
    get_resource_client,
    get_user_client,
    oauth2_scheme,
)
from src.services.clients import GroupClient, PermissionClient, ResourceClient, UserClient

router = APIRouter(prefix="/database", tags=["Database"])


@router.get("/users")
async def get_users(token: str = Depends(oauth2_scheme), client: UserClient = Depends(get_user_client)):
    return await client.get_all(token=token)


@router.get("/user-groups", include_in_schema=False)
async def get_user_groups(
    user_id: UUID, token: str = Depends(oauth2_scheme), client: UserClient = Depends(get_user_client)
):
    return await client.get_groups(user_id=user_id, token=token)


@router.get("/user-permissions")
async def get_user_permissions(
    user_id: UUID, token: str = Depends(oauth2_scheme), client: UserClient = Depends(get_user_client)
):
    return await client.get_permissions(user_id=user_id, token=token)


@router.get("/user-resources")
async def get_user_resources(
    user_id: UUID, token: str = Depends(oauth2_scheme), client: UserClient = Depends(get_user_client)
):
    return await client.get_resources(user_id=user_id, token=token)


@router.get("/users/{id}", include_in_schema=False)
async def get_user(id: UUID, token: str = Depends(oauth2_scheme), client: UserClient = Depends(get_user_client)):
    return await client.get(user_id=id, token=token)


@router.get("/groups")
async def get_groups(token: str = Depends(oauth2_scheme), client: GroupClient = Depends(get_group_client)):
    return await client.get_all(token=token)


@router.get("/groups/{id}", include_in_schema=False)
async def get_group(
    id: PositiveInt, token: str = Depends(oauth2_scheme), client: GroupClient = Depends(get_group_client)
):
    return await client.get(group_id=id, token=token)


@router.get("/permissions")
async def get_permissions(
    token: str = Depends(oauth2_scheme), client: PermissionClient = Depends(get_permission_client)
):
    return await client.get_all(token=token)


@router.get("/permissions/{id}", include_in_schema=False)
async def get_permission(
    id: PositiveInt, token: str = Depends(oauth2_scheme), client: PermissionClient = Depends(get_permission_client)
):
    return await client.get(permission_id=id, token=token)


@router.get("/resources")
async def get_resources(token: str = Depends(oauth2_scheme), client: ResourceClient = Depends(get_resource_client)):
    return await client.get_all(token=token)


@router.get("/resources/{id}", include_in_schema=False)
async def get_resource(
    id: PositiveInt, token: str = Depends(oauth2_scheme), client: ResourceClient = Depends(get_resource_client)
):
    return await client.get(resource_id=id, token=token)
