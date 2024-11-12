from fastapi import APIRouter, Depends

from api.db.models import User
from api.services.market import MarketService
from api.utils import get_current_user

router = APIRouter(
    prefix='/get/all',
)


@router.get('')
async def route(user: User = Depends(get_current_user)):
    result = await MarketService().cart_get(user=user)
    return result
