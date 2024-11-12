from fastapi import APIRouter

from .calculator import router as router_get_calculator_data
from .cart import router as router_cart

router = APIRouter(
    prefix='/market',
    tags=['Market'],
)
routers = [router_cart, router_get_calculator_data]
[router.include_router(router_) for router_ in routers]
