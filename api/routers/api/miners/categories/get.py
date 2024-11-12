from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.miners_categories import MinerCategoryService

router = APIRouter(
    prefix='/get',
)


class MarketCategoryGetSchema(BaseModel):
    id: int


@router.get('')
async def route(schema: MarketCategoryGetSchema = Depends()):
    result = await MinerCategoryService().get(id_=schema.id)
    return result
