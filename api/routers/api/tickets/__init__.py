from fastapi import APIRouter

from .close import router as router_close
from .create import router as router_create
from .get import router as router_get
from .get_all import router as router_get_all
from .messages import router as router_messages
from .sort import router as router_sort

router = APIRouter(
    prefix="/tickets",
    tags=['Tickets'],
)
routers = [
    router_create, router_get, router_get_all, router_close,
    router_messages, router_sort, 
]
[router.include_router(router_) for router_ in routers]
