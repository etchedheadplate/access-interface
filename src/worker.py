from src.config import Settings
from src.logger import logger
from src.queue.producer import send_message
from src.services.status.schemas import StatusCreatedResponse, StatusUnprocessableResponse
from src.services.tasks.creators import (
    AccessPermissionTask,
    ExcludeFromGroupTask,
    GetResourcePermissionTask,
    JoinGroupTask,
    RemovePermissionTask,
    ViewUserGroupsTask,
)


class RequestWorker:
    def __init__(
        self,
        task: (
            AccessPermissionTask
            | ExcludeFromGroupTask
            | GetResourcePermissionTask
            | JoinGroupTask
            | RemovePermissionTask
            | ViewUserGroupsTask
        ),
    ):
        settings = Settings()  # type: ignore[call-arg]
        self.task_routing_key = settings.ROUTING_KEY_TASK
        self.status_routing_key = settings.ROUTING_KEY_STATUS_CREATED
        self.exchange_name = settings.EXCHANGE_NAME
        self.task = task
        self.error = self._is_unprocessable()
        self.status = self._create_status()

    def _is_unprocessable(self):
        return self.task.error

    def _create_status(self):
        if not self.error:
            return StatusCreatedResponse(request_id=self.task.request_id)
        else:
            return StatusUnprocessableResponse(request_id="")

    async def send_request(self):
        if not self.error:
            await send_message(self.exchange_name, self.task_routing_key, self.task.model_dump())
            logger.info(f"OUT: request_id={self.task.request_id}, request_status={self.task.request_type}")
        await send_message(self.exchange_name, self.status_routing_key, self.status.model_dump())
        logger.info(f"OUT: request_id={self.status.request_id}, request_status={self.status.request_status}")
        return self.status
