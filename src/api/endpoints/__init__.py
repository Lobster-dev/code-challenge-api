from fastapi import APIRouter

from .age_group import router as age_group_router
from .enrollment import router as enrollment_router
from .health_check import router as health_check_router

public_router = APIRouter()
private_router = APIRouter(prefix="/api/v1")

public_router.include_router(health_check_router)
private_router.include_router(age_group_router)
private_router.include_router(enrollment_router)

__all__ = ["public_router", "private_router"]