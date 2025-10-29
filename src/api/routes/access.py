from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import PositiveInt

from src.queue import EXCHANGE_NAME, ROUTING_KEY_STATUS, ROUTING_KEY_TASK, send_message
from src.services import (
    AccessPermissionRequest,
    ExcludeFromGroupRequest,
    GetResourcePermissionRequest,
    JoinGroupRequest,
    RemovePermissionRequest,
    ViewUserGroups,
    access_permission,
    exclude_from_group,
    get_resource_permission,
    join_group,
    remove_permission,
    view_user_groups,
)

load_dotenv()

router = APIRouter(prefix="/request", tags=["Request"])


@router.get("/permission-access")
async def request_permission_access(user_id: UUID, permission_id: PositiveInt):
    task: AccessPermissionRequest | None = await access_permission(user_id, permission_id)
    if not task:
        return {"message": f"User '{user_id}' already has permission '{permission_id}'"}

    await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task)

    status_message = {
        "request_id": task.request_id,
        "request_status": "created",
    }
    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status_message)

    return status_message


@router.get("/join-group")
async def request_join_group(user_id: UUID, group_id: PositiveInt):
    task: JoinGroupRequest | None = await join_group(user_id, group_id)
    if not task:
        return {"message": f"User '{user_id}' already in group '{group_id}'"}

    await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task)

    status_message = {
        "request_id": task.request_id,
        "request_status": "created",
    }
    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status_message)

    return status_message


@router.get("/remove-permission")
async def request_remove_permission(user_id: UUID, permission_id: PositiveInt):
    task: RemovePermissionRequest | None = await remove_permission(user_id, permission_id)
    if not task:
        return {"message": f"User '{user_id}' do not have permission '{permission_id}'"}

    await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task)

    status_message = {
        "request_id": task.request_id,
        "request_status": "created",
    }
    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status_message)

    return status_message


@router.get("/exclude-from-group")
async def request_exclude_from_group(user_id: UUID, group_id: PositiveInt):
    task: ExcludeFromGroupRequest | None = await exclude_from_group(user_id, group_id)
    if not task:
        return {"message": f"User '{user_id}' is not in group '{group_id}'"}

    await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task)

    status_message = {
        "request_id": task.request_id,
        "request_status": "created",
    }
    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status_message)

    return status_message


@router.get("/view-user-groups")
async def request_view_user_groups(user_id: UUID):
    task: ViewUserGroups | None = await view_user_groups(user_id)
    if not task:
        return {"message": f"User '{user_id}' does not exist"}

    await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task)

    status_message = {
        "request_id": task.request_id,
        "request_status": "created",
    }
    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status_message)

    return status_message


@router.get("/get-resource-permission")
async def request_get_resource_permission(user_id: UUID, resource_id: PositiveInt):
    task: GetResourcePermissionRequest | None = await get_resource_permission(user_id, resource_id)
    if not task:
        return {"message": f"Resource '{resource_id}' does not exist"}

    await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task)

    status_message = {
        "request_id": task.request_id,
        "request_status": "created",
    }
    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status_message)

    return status_message
