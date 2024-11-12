from fastapi import APIRouter

from .balance import router as router_balance
from .categories import router as router_categories
from .dashboards import router as router_dashboards
from .get import router as router_get
from .get_all import router as router_get_all
from .workers import router as router_get_workers
from .information import router as router_information
from .payments import router as router_payments

router = APIRouter(
    prefix="/miners",
    tags=['Miners'],
)
routers = [
    router_get, router_get_all,
    router_categories,
    router_balance, router_dashboards, router_get_workers, router_payments, router_information,
]
[router.include_router(router_) for router_ in routers]
