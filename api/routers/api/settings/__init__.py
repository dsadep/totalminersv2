from fastapi import APIRouter

from .get import router as router_get
from .get_all import router as router_get_all

router = APIRouter(
    prefix="/settings",
    tags=['Settings'],
)
routers = [
    router_get, router_get_all,
]

[router.include_router(router_) for router_ in routers]
