from fastapi import APIRouter, Depends

from api.services.miners import MinerService
from api.utils import get_current_user

router = APIRouter(
    prefix='/information',
)


@router.get('')
async def route(user=Depends(get_current_user)):
    result = await MinerService().information(user=user)
    return result
