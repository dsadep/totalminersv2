from fastapi import APIRouter

from .create import router as router_create
from .delete import router as router_delete
from .get import router as router_get

router = APIRouter(
    prefix='/images',
    tags=['Images'],
)
routers = [router_create, router_get, router_delete]
[router.include_router(router_) for router_ in routers]
