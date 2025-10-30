from pydantic import BaseModel


class StatusCreatedResponse(BaseModel):
    request_id: str
    request_status: str = "created"


class StatusRejectedResponse(BaseModel):
    request_id: str
    request_status: str = "rejected"
