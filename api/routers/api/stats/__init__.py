from fastapi import APIRouter

from .all import router as router_all
from .daily import router as router_daily
from .weekly import router as router_weekly
from .monthly import router as router_monthly


router = APIRouter(
    prefix='/stats',
    tags=['Stats']
)

router.include_router(router_all)
router.include_router(router_daily)
router.include_router(router_weekly)
router.include_router(router_monthly)