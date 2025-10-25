from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.auth.routes import router_auth
from src.api.service.routes import router_service

load_dotenv()

app = FastAPI()
app.include_router(router_service)
app.include_router(router_auth)
