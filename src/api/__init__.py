from fastapi import APIRouter

from .access.routes import router as access_router
from .auth.routes import router as auth_router
from .database import router as database_router
from .ping import router as health_router

router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(access_router)
router.include_router(database_router)

__all__ = ["router"]
