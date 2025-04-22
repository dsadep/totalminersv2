from fastapi import APIRouter

from .get import router as router_get

router = APIRouter(
    prefix='/stats',
    tags=['Stats']
)

router.include_router(router_get)