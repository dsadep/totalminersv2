from fastapi import APIRouter

from .get_for_user import router as router_get_for_user


router = APIRouter(
    prefix='/discounts',
    tags=['Discounts'],
)
routers = [router_get_for_user]
[router.include_router(router_) for router_ in routers]
