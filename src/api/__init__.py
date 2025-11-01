from fastapi import APIRouter

from .auth.routes import router as auth_router
from .database import router as database_router
from .ping import router as health_router
from .request import router as request_router

router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(database_router)
router.include_router(request_router)

__all__ = ["router"]
