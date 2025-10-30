from uuid import UUID

from pydantic import PositiveInt

from src.api.config import Routes
from src.services.schemas import (
    AccessPermissionRequest,
    ExcludeFromGroupRequest,
    GetResourcePermissionRequest,
    JoinGroupRequest,
    RemovePermissionRequest,
    ViewUserGroups,
)
from src.services.utils import call_route, generate_id


async def access_permission(user_id: UUID, permission_id: PositiveInt) -> AccessPermissionRequest:
    request_id = await generate_id()
    error = False
    user_id_str = str(user_id)

    try:
        get_permission_groups = await call_route(
            route=Routes.Private.Permission.GROUPS, params={"permission_id": permission_id}
        )
        permission_groups = [group["name"] for group in get_permission_groups]

        get_user_groups = await call_route(route=Routes.Private.User.GROUPS, params={"user_id": user_id_str})
        user_groups = [group["name"] for group in get_user_groups]

    except Exception:
        error = True
        permission_groups = []
        user_groups = []

    return AccessPermissionRequest(
        request_id=request_id,
        user_id=user_id_str,
        permission_id=permission_id,
        permission_groups=permission_groups,
        user_groups=user_groups,
        error=error,
    )


async def join_group(user_id: UUID, group_id: PositiveInt) -> JoinGroupRequest:
    request_id = await generate_id()
    error = False
    user_id_str = str(user_id)

    try:
        get_user_groups = await call_route(route=Routes.Private.User.GROUPS, params={"user_id": user_id_str})
        user_groups = [group["name"] for group in get_user_groups]

        get_user_permissions = await call_route(route=Routes.Private.User.PERMISSIONS, params={"user_id": user_id_str})
        user_permissions = [permission["name"] for permission in get_user_permissions]

    except Exception:
        error = True
        user_groups = []
        user_permissions = []

    return JoinGroupRequest(
        request_id=request_id,
        user_id=user_id_str,
        group_id=group_id,
        user_groups=user_groups,
        user_permissions=user_permissions,
        error=error,
    )


async def remove_permission(user_id: UUID, permission_id: PositiveInt) -> RemovePermissionRequest:
    request_id = await generate_id()
    error = False
    user_id_str = str(user_id)

    return RemovePermissionRequest(
        request_id=request_id,
        user_id=user_id_str,
        permission_id=permission_id,
        error=error,
    )


async def exclude_from_group(user_id: UUID, group_id: PositiveInt) -> ExcludeFromGroupRequest:
    request_id = await generate_id()
    error = False
    user_id_str = str(user_id)

    return ExcludeFromGroupRequest(
        request_id=request_id,
        user_id=user_id_str,
        group_id=group_id,
        error=error,
    )


async def view_user_groups(user_id: UUID) -> ViewUserGroups:
    request_id = await generate_id()
    error = False
    user_id_str = str(user_id)

    return ViewUserGroups(
        request_id=request_id,
        user_id=user_id_str,
        error=error,
    )


async def get_resource_permission(user_id: UUID, resource_id: PositiveInt) -> GetResourcePermissionRequest:
    request_id = await generate_id()
    error = False
    user_id_str = str(user_id)

    return GetResourcePermissionRequest(
        request_id=request_id,
        user_id=user_id_str,
        resource_id=resource_id,
        error=error,
    )
