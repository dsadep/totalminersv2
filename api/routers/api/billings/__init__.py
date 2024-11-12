from fastapi import APIRouter

from .get import router as router_get
from .get_all import router as router_get_all
from .updates import router as router_updates

router = APIRouter(
    prefix='/billings',
    tags=['Billings'],
)
routers = [router_get, router_get_all, router_updates]
[router.include_router(router_) for router_ in routers]
