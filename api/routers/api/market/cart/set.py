from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.market import MarketService
from api.utils import get_current_user

router = APIRouter(
    prefix='/set',
)


class MarketCartSetSchema(BaseModel):
    miner_item_id: int
    count: int


@router.get('')
async def route(schema: MarketCartSetSchema = Depends(), user: User = Depends(get_current_user)):
    result = await MarketService().cart_set(
        user=user,
        miner_item_id=schema.miner_item_id,
        count=schema.count,
    )
    return result
