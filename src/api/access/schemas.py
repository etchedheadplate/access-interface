from pydantic import BaseModel


class StatusCreatedResponse(BaseModel):
    request_id: str
    request_status: str = "created"


class StatusUnprocessableResponse(BaseModel):
    request_id: str
    request_status: str = "unprocessable"
