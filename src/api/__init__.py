from fastapi import APIRouter

from .routes.access import router as access_router
from .routes.auth import router as auth_router
from .routes.database import router as database_router
from .routes.health import router as health_router

router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(access_router)
router.include_router(database_router)

__all__ = ["router"]
