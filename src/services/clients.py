from collections.abc import Mapping
from typing import Any
from urllib.parse import urljoin
from uuid import UUID

import httpx

from src.api.schemas import LoginRequest, RegisterRequest
from src.config import Settings


class Client:
    def __init__(self, timeout: float = 10.0):
        settings = Settings()  # type: ignore[call-arg]
        self._base = settings.DB_SERVICE_BASE_URL
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb):  # type: ignore
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def create_url(self, endpoint: str) -> str:
        base = self._base.rstrip("/") + "/"
        endpoint = endpoint.lstrip("/")
        return urljoin(base, endpoint)

    @staticmethod
    def create_headers(token: str | None = None) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    async def _request(
        self,
        method: str,
        endpoint: str,
        token: str | None = None,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> Any:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)

        url = self.create_url(endpoint)
        headers = self.create_headers(token) if token else {}

        response = await self._client.request(
            method=method, url=url, headers=headers, params=params, json=json, data=data
        )
        response.raise_for_status()
        return response.json()


class UserClient(Client):
    _register_endpoint = "/auth/register"
    _login_endpoint = "/auth/login"
    _get_endpoint = "/database/users/"
    _get_groups_endpoint = "/access/view/user-groups"
    _get_permissions_endpoint = "/access/view/user-permissions"
    _get_resources_endpoint = "/access/view/user-resources"

    async def register(self, request: RegisterRequest) -> dict[str, Any]:
        return await self._request("POST", self._register_endpoint, json=request.model_dump())

    async def login(self, request: LoginRequest) -> dict[str, Any]:
        return await self._request("POST", self._login_endpoint, data=request.model_dump())

    async def get(self, user_id: UUID, token: str | None = None) -> dict[str, Any]:
        endpoint = f"{self._get_endpoint}{user_id}/"
        return await self._request("GET", endpoint, token=token)

    async def get_all(self, token: str | None = None) -> dict[str, Any]:
        return await self._request("GET", self._get_endpoint, token=token)

    async def get_groups(self, user_id: UUID, token: str | None = None) -> dict[str, Any]:
        params = {"user_id": user_id}
        return await self._request("GET", self._get_groups_endpoint, token=token, params=params)

    async def get_permissions(self, user_id: UUID, token: str | None = None) -> dict[str, Any]:
        params = {"user_id": user_id}
        return await self._request("GET", self._get_permissions_endpoint, token=token, params=params)

    async def get_resources(self, user_id: UUID, token: str | None = None) -> dict[str, Any]:
        params = {"user_id": user_id}
        return await self._request("GET", self._get_resources_endpoint, token=token, params=params)


class GroupClient(Client):
    _get_endpoint = "/database/groups/"
    _get_users_endpoint = "/access/view/group-users"
    _get_permissions_endpoint = "/access/view/group-permissions"
    _get_resources_endpoint = "/access/view/group-resources"

    async def get(self, group_id: int, token: str | None = None) -> dict[str, Any]:
        endpoint = f"{self._get_endpoint}{group_id}/"
        return await self._request("GET", endpoint, token=token)

    async def get_all(self, token: str | None = None) -> dict[str, Any]:
        return await self._request("GET", self._get_endpoint, token=token)

    async def get_users(self, group_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"group_id": group_id}
        return await self._request("GET", self._get_users_endpoint, token=token, params=params)

    async def get_permissions(self, group_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"group_id": group_id}
        return await self._request("GET", self._get_permissions_endpoint, token=token, params=params)

    async def get_resources(self, group_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"group_id": group_id}
        return await self._request("GET", self._get_resources_endpoint, token=token, params=params)


class PermissionClient(Client):
    _get_endpoint = "/database/permissions/"
    _get_groups_endpoint = "/access/view/permission-groups"
    _get_users_endpoint = "/access/view/permission-users"
    _get_resources_endpoint = "/access/view/permission-resources"

    async def get(self, permission_id: int, token: str | None = None) -> dict[str, Any]:
        endpoint = f"{self._get_endpoint}{permission_id}/"
        return await self._request("GET", endpoint, token=token)

    async def get_all(self, token: str | None = None) -> dict[str, Any]:
        return await self._request("GET", self._get_endpoint, token=token)

    async def get_groups(self, permission_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"permission_id": permission_id}
        return await self._request("GET", self._get_groups_endpoint, token=token, params=params)

    async def get_users(self, permission_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"permission_id": permission_id}
        return await self._request("GET", self._get_users_endpoint, token=token, params=params)

    async def get_resources(self, permission_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"permission_id": permission_id}
        return await self._request("GET", self._get_resources_endpoint, token=token, params=params)


class ResourceClient(Client):
    _get_endpoint = "/database/resources/"
    _get_users_endpoint = "/access/view/resource-users"
    _get_groups_endpoint = "/access/view/resource-groups"
    _get_permissions_endpoint = "/access/view/resource-permissions"

    async def get(self, resource_id: int, token: str | None = None) -> dict[str, Any]:
        endpoint = f"{self._get_endpoint}{resource_id}/"
        return await self._request("GET", endpoint, token=token)

    async def get_all(self, token: str | None = None) -> dict[str, Any]:
        return await self._request("GET", self._get_endpoint, token=token)

    async def get_users(self, resource_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"resource_id": resource_id}
        return await self._request("GET", self._get_users_endpoint, token=token, params=params)

    async def get_groups(self, resource_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"resource_id": resource_id}
        return await self._request("GET", self._get_groups_endpoint, token=token, params=params)

    async def get_permissions(self, resource_id: int, token: str | None = None) -> dict[str, Any]:
        params = {"resource_id": resource_id}
        return await self._request("GET", self._get_permissions_endpoint, token=token, params=params)
