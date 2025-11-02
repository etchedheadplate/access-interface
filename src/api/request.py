from uuid import UUID

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from pydantic import PositiveInt

from src.api.auth import oauth2_scheme
from src.logger import logger
from src.queue import EXCHANGE_NAME, ROUTING_KEY_STATUS_CREATED, ROUTING_KEY_TASK, send_message
from src.services.status.schemas import (
    BaseStatus,
    StatusCreatedResponse,
    StatusNotFoundResponse,
    StatusUnprocessableResponse,
)
from src.services.tasks.creators import get_task_creator

load_dotenv()

router = APIRouter(prefix="/request", tags=["Request"])
create_router = APIRouter(prefix="/create")


@router.get("/status", response_model=BaseStatus)
async def check_request_status(request: Request, request_id: str, token: str = Depends(oauth2_scheme)):
    try:
        last_status_message = request.app.state.last_status_message()
        return last_status_message[request_id]
    except Exception:
        return StatusNotFoundResponse(request_id=request_id)


@create_router.post("/add-to-group", response_model=BaseStatus)
async def request_add_user_to_group(user_id: UUID, group_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    request_type = "join_group"
    request = get_task_creator(request_type, user_id)
    task = await request.create(group_id=group_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        logger.info(f"OUT: request_id={task.request_id}, request_status={task.request_type}")
        message_out = StatusCreatedResponse(request_id=task.request_id)
    else:
        message_out = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS_CREATED, message_out.model_dump())
    logger.info(f"OUT: request_id={message_out.request_id}, request_status={message_out.request_status}")

    return message_out


@create_router.post("/remove-from-group", response_model=BaseStatus)
async def request_remove_user_from_group(user_id: UUID, group_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    request_type = "exclude_from_group"
    request = get_task_creator(request_type, user_id)
    task = await request.create(group_id=group_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        logger.info(f"OUT: request_id={task.request_id}, request_status={task.request_type}")
        message_out = StatusCreatedResponse(request_id=task.request_id)
    else:
        message_out = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS_CREATED, message_out.model_dump())
    logger.info(f"OUT: request_id={message_out.request_id}, request_status={message_out.request_status}")

    return message_out


@create_router.post("/view-user-groups", response_model=BaseStatus)
async def request_view_user_groups(user_id: UUID, token: str = Depends(oauth2_scheme)):
    request_type = "view_user_groups"
    request = get_task_creator(request_type, user_id)
    task = await request.create()
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        logger.info(f"OUT: request_id={task.request_id}, request_status={task.request_type}")
        message_out = StatusCreatedResponse(request_id=task.request_id)
    else:
        message_out = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS_CREATED, message_out.model_dump())
    logger.info(f"OUT: request_id={message_out.request_id}, request_status={message_out.request_status}")

    return message_out


@create_router.post("/add-permission", response_model=BaseStatus)
async def request_add_permission_to_user(
    user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    request_type = "access_permission"
    request = get_task_creator(request_type, user_id)
    task = await request.create(permission_id=permission_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        logger.info(f"OUT: request_id={task.request_id}, request_status={task.request_type}")
        message_out = StatusCreatedResponse(request_id=task.request_id)
    else:
        message_out = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS_CREATED, message_out.model_dump())
    logger.info(f"OUT: request_id={message_out.request_id}, request_status={message_out.request_status}")

    return message_out


@create_router.post("/remove-permission", response_model=BaseStatus)
async def request_remove_permission_from_user(
    user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    request_type = "remove_permission"
    request = get_task_creator(request_type, user_id)
    task = await request.create(permission_id=permission_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        logger.info(f"OUT: request_id={task.request_id}, request_status={task.request_type}")
        message_out = StatusCreatedResponse(request_id=task.request_id)
    else:
        message_out = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS_CREATED, message_out.model_dump())
    logger.info(f"OUT: request_id={message_out.request_id}, request_status={message_out.request_status}")

    return message_out


@create_router.post("/view-resource-permission", response_model=BaseStatus)
async def request_view_resource_permission(
    user_id: UUID, resource_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    request_type = "get_resource_permission"
    request = get_task_creator(request_type, user_id)
    task = await request.create(resource_id=resource_id)
    if not task.error:
        await send_message(EXCHANGE_NAME, ROUTING_KEY_TASK, task.model_dump())
        logger.info(f"OUT: request_id={task.request_id}, request_status={task.request_type}")
        message_out = StatusCreatedResponse(request_id=task.request_id)
    else:
        message_out = StatusUnprocessableResponse(request_id="")

    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS_CREATED, message_out.model_dump())
    logger.info(f"OUT: request_id={message_out.request_id}, request_status={message_out.request_status}")

    return message_out


router.include_router(create_router)
