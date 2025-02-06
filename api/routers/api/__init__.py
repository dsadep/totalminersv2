from fastapi import APIRouter

from .auth import router as router_auth
from .billings import router as router_billings
from .feedbacks import router as router_feedback
from .images import router as router_image
from .market import router as router_market
from .miners import router as router_miner
from .settings import router as router_settings
from .tickets import router as router_ticket
from .users import router as router_users
from .discounts import router as router_discounts
from .test import router as router_test

router = APIRouter(
    prefix='/api',
)
routers = [
    router_auth, router_users, router_market, router_billings, router_miner, router_ticket, router_feedback,
    router_image, router_settings, router_discounts,router_test,
]
[router.include_router(router_) for router_ in routers]
