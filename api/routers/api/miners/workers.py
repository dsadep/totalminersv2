from fastapi import APIRouter, Depends

from api.services.headframe import HeadframeService
from api.services.miners import MinerService
from api.utils import get_current_user

router = APIRouter(
    prefix='/workers',
)


@router.get('')
async def route(user=Depends(get_current_user)):
    result = await MinerService().get_workers(user=user)
    return result
