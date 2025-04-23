from fastapi import APIRouter, Depends

from api.services.stats import StatsService
from api.utils import get_current_user

router = APIRouter(
    prefix='/monthly'
)

@router.get('')
async def get_stats(current_user=Depends(get_current_user)):
    stats = await StatsService().get_stats(current_user.id, days=30)
    return stats