from fastapi.security import OAuth2PasswordBearer

from src.services.clients import GroupClient, PermissionClient, ResourceClient, UserClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_user_client():
    async with UserClient() as client:
        yield client


async def get_group_client():
    async with GroupClient() as client:
        yield client


async def get_permission_client():
    async with PermissionClient() as client:
        yield client


async def get_resource_client():
    async with ResourceClient() as client:
        yield client
