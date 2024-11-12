from fastapi import APIRouter

from .buy import router as router_buy
from .get_all import router as router_get_all
from .set import router as router_set

router = APIRouter(
    prefix='/cart',
)
routers = [router_set, router_get_all, router_buy]
[router.include_router(router_) for router_ in routers]
