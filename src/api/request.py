from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from pydantic import PositiveInt

from src.api.auth import oauth2_scheme
from src.queue import EXCHANGE_NAME, ROUTING_KEY_STATUS, ROUTING_KEY_TASK, send_message
from src.services.status.schemas import BaseStatus, StatusCreatedResponse, StatusUnprocessableResponse
from src.services.tasks.creators import get_task_creator

load_dotenv()

router = APIRouter(prefix="/request", tags=["Request"])
create_router = APIRouter(prefix="/create")


@router.get("/status", response_model=BaseStatus)
async def check_status(request: Request, request_id: str, token: str = Depends(oauth2_scheme)):
    last_status_message = request.app.state.last_status_message()

    if not last_status_message:
        return BaseStatus(
            request_id=request_id,
            request_status="not_found",
            request_result="No status messages yet",
        )

    if last_status_message.get("request_id") != request_id:
        return BaseStatus(
            request_id=request_id,
            request_status="not_found",
            request_result="No matching request_id in recent messages",
        )

    status_obj = BaseStatus(**last_status_message)
    return status_obj


@create_router.get("/permission-access")
async def request_permission_access(user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    request_type = "access_permission"
    request = get_task_creator(request_type, user_id)
    task = await request.create(permission_id=permission_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@create_router.get("/join-group")
async def request_join_group(user_id: UUID, group_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    request_type = "join_group"
    request = get_task_creator(request_type, user_id)
    task = await request.create(group_id=group_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@create_router.get("/remove-permission")
async def request_remove_user_permission(
    user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    request_type = "remove_permission"
    request = get_task_creator(request_type, user_id)
    task = await request.create(permission_id=permission_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@create_router.get("/exclude-from-group")
async def request_exclude_user_from_group(user_id: UUID, group_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    request_type = "exclude_from_group"
    request = get_task_creator(request_type, user_id)
    task = await request.create(group_id=group_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@create_router.get("/view-user-groups")
async def request_view_user_groups(user_id: UUID, token: str = Depends(oauth2_scheme)):
    request_type = "view_user_groups"
    request = get_task_creator(request_type, user_id)
    task = await request.create()
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


@create_router.get("/get-resource-permission")
async def request_get_resource_permission(user_id: UUID, resource_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    request_type = "get_resource_permission"
    request = get_task_creator(request_type, user_id)
    task = await request.create(resource_id=resource_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        status = StatusCreatedResponse(request_id=task.request_id)
    else:
        status = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, status.model_dump())

    return status


router.include_router(create_router)
