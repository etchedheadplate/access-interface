from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.auth.routes import router_auth
from src.api.health.routes import router_health

load_dotenv()

app = FastAPI()
app.include_router(router_health)
app.include_router(router_auth)
