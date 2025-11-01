from typing import Any

from src.services.status.schemas import (
    StatusCreatedResponse,
    StatusDoneResponse,
    StatusRejectedResponse,
    StatusUnprocessableResponse,
    StatusValidatedResponse,
)


class StatusProcessor:
    def __init__(self, message: dict[str, Any]):
        self.message = message
        self.request_id = message["request_id"]
        self.request_status = message["request_status"]
        self.is_appropriate = self._is_appropriate()

    def _is_appropriate(self) -> bool:
        return self.request_status in StatusMapping.STATUS

    async def process(self, task_validated: bool, task_result: str | list[str]):
        self.request_result = task_result
        schema = StatusMapping.STATUS[self.request_status]
        if task_validated:
            return schema(request_id=self.request_id, request_result=self.request_result)


class StatusMapping:
    STATUS = {
        "created": StatusCreatedResponse,
        "validated": StatusValidatedResponse,
        "rejected": StatusRejectedResponse,
        "done": StatusDoneResponse,
        "unprocessable": StatusUnprocessableResponse,
    }
