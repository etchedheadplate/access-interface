from fastapi import APIRouter

from src.api.routes.auth import router as auth_router
from src.api.routes.database import router as database_router
from src.api.routes.ping import router as health_router
from src.api.routes.request import router as request_router

router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(database_router)
router.include_router(request_router)

__all__ = ["router"]
