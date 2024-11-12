from fastapi import APIRouter

from .create import router as router_create
from .get_all import router as router_get

router = APIRouter(
    prefix="/messages",
)
routers = [
    router_create, router_get,
]
[router.include_router(router_) for router_ in routers]
