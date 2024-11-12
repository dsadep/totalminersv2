from fastapi import APIRouter

from .cancel import router as router_cancel
from .complete import router as router_complete
from .payment_type import router as router_payment_type

router = APIRouter(
    prefix='/update',
)
routers = [router_payment_type, router_complete, router_cancel]
[router.include_router(router_) for router_ in routers]
