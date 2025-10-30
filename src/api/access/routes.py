from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.api.auth import oauth2_scheme
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

from .schemas import StatusCreatedResponse, StatusUnprocessableResponse

load_dotenv()

router = APIRouter(prefix="/request", tags=["Request"])


@router.get("/permission-access")
async def request_permission_access(user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    task: AccessPermissionRequest = await access_permission(user_id, permission_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@router.get("/join-group")
async def request_join_group(user_id: UUID, group_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    task: JoinGroupRequest = await join_group(user_id, group_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@router.get("/remove-permission")
async def request_remove_user_permission(
    user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    task: RemovePermissionRequest = await remove_permission(user_id, permission_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@router.get("/exclude-from-group")
async def request_exclude_user_from_group(user_id: UUID, group_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    task: ExcludeFromGroupRequest = await exclude_from_group(user_id, group_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@router.get("/view-user-groups")
async def request_view_user_groups(user_id: UUID, token: str = Depends(oauth2_scheme)):
    task: ViewUserGroups = await view_user_groups(user_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@router.get("/get-resource-permission")
async def request_get_resource_permission(user_id: UUID, resource_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    task: GetResourcePermissionRequest = await get_resource_permission(user_id, resource_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status
