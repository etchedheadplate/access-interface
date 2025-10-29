from uuid import UUID

from pydantic import PositiveInt

from api.config import Routes
from services.schemas import (
    AccessPermissionRequest,
    ExcludeFromGroupRequest,
    GetResourcePermissionRequest,
    JoinGroupRequest,
    RemovePermissionRequest,
    ViewUserGroups,
)
from services.utils import call_route, generate_id


async def access_permission(user_id: UUID, permission_id: PositiveInt) -> AccessPermissionRequest | None:
    """
    TODO
    has_permission = await call_route(route=Routes.Private.User.HAS_PERMISSION, params={"user_id": user_id})
    if has_permission:
        return None
    """
    request_id = await generate_id()

    get_permission_groups = await call_route(route=Routes.Private.Permission.GROUPS)
    permission_groups = [group["name"] for group in get_permission_groups]

    get_user_groups = await call_route(route=Routes.Private.User.GROUPS)
    user_groups = [group["name"] for group in get_user_groups]

    return AccessPermissionRequest(
        request_id=request_id,
        user_id=user_id,
        permission_id=permission_id,
        permission_groups=permission_groups,
        user_groups=user_groups,
    )


async def join_group(user_id: UUID, group_id: PositiveInt) -> JoinGroupRequest | None:
    """
    TODO
    in_group = await call_route(route=Routes.Private.User.IN_GROUP, params={"user_id": user_id})
    if in_group:
        return None
    """
    request_id = await generate_id()

    get_user_groups = await call_route(route=Routes.Private.User.GROUPS)
    user_groups = [group["name"] for group in get_user_groups]

    get_user_permissions = await call_route(route=Routes.Private.User.PERMISSIONS)
    user_permissions = [permission["name"] for permission in get_user_permissions]

    return JoinGroupRequest(
        request_id=request_id,
        user_id=user_id,
        group_id=group_id,
        user_groups=user_groups,
        user_permissions=user_permissions,
    )


async def remove_permission(user_id: UUID, permission_id: PositiveInt) -> RemovePermissionRequest | None:
    """
    TODO
    has_permission = await call_route(route=Routes.Private.User.HAS_PERMISSION, params={"user_id": user_id})
    if not has_permission:
        return None
    """
    request_id = await generate_id()

    return RemovePermissionRequest(
        request_id=request_id,
        user_id=user_id,
        permission_id=permission_id,
    )


async def exclude_from_group(user_id: UUID, group_id: PositiveInt) -> ExcludeFromGroupRequest | None:
    """
    TODO
    in_group = await call_route(route=Routes.Private.User.IN_GROUP, params={"user_id": user_id})
    if not in_group:
        return None
    """
    request_id = await generate_id()

    return ExcludeFromGroupRequest(
        request_id=request_id,
        user_id=user_id,
        group_id=group_id,
    )


async def view_user_groups(user_id: UUID) -> ViewUserGroups | None:
    """
    TODO check if user exists?
    """
    request_id = await generate_id()

    return ViewUserGroups(
        request_id=request_id,
        user_id=user_id,
    )


async def get_resource_permission(user_id: UUID, resource_id: PositiveInt) -> GetResourcePermissionRequest | None:
    """
    TODO check if resource exists?
    """
    request_id = await generate_id()

    return GetResourcePermissionRequest(request_id=request_id, user_id=user_id, resource_id=resource_id)
