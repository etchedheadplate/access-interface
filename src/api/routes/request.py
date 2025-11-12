from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import PositiveInt

from src.api.dependancies import oauth2_scheme
from src.services.status.schemas import BaseStatus, StatusNotFoundResponse
from src.services.tasks.creators import get_task_creator
from src.worker import RequestWorker

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
    creator = get_task_creator("join_group", user_id)
    task = await creator.create(group_id=group_id)
    worker = RequestWorker(task)
    return await worker.send_request()


@create_router.post("/remove-from-group", response_model=BaseStatus)
async def request_remove_user_from_group(user_id: UUID, group_id: PositiveInt, token: str = Depends(oauth2_scheme)):
    creator = get_task_creator("exclude_from_group", user_id)
    task = await creator.create(group_id=group_id)
    worker = RequestWorker(task)
    return await worker.send_request()


@create_router.post("/view-user-groups", response_model=BaseStatus)
async def request_view_user_groups(user_id: UUID, token: str = Depends(oauth2_scheme)):
    creator = get_task_creator("view_user_groups", user_id)
    task = await creator.create()
    worker = RequestWorker(task)
    return await worker.send_request()


@create_router.post("/add-permission", response_model=BaseStatus)
async def request_add_permission_to_user(
    user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    creator = get_task_creator("access_permission", user_id)
    task = await creator.create(permission_id=permission_id)
    worker = RequestWorker(task)
    return await worker.send_request()


@create_router.post("/remove-permission", response_model=BaseStatus)
async def request_remove_permission_from_user(
    user_id: UUID, permission_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    creator = get_task_creator("remove_permission", user_id)
    task = await creator.create(permission_id=permission_id)
    worker = RequestWorker(task)
    return await worker.send_request()


@create_router.post("/view-resource-permission", response_model=BaseStatus)
async def request_view_resource_permission(
    user_id: UUID, resource_id: PositiveInt, token: str = Depends(oauth2_scheme)
):
    creator = get_task_creator("get_resource_permission", user_id)
    task = await creator.create(resource_id=resource_id)
    worker = RequestWorker(task)
    return await worker.send_request()


router.include_router(create_router)
