from fastapi import APIRouter, Depends

from api.services.miners import MinerService
from api.utils import get_current_user

router = APIRouter(
    prefix='/dashboards',
)


@router.get('')
async def route(user=Depends(get_current_user)):
    result = await MinerService().dashboards(user=user)
    return result
