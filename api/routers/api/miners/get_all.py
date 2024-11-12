from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.services.miners import MinerService

router = APIRouter(
    prefix='/get/all',
)


class MinerGetAllSchema(BaseModel):
    category_id: Optional[int] = Field(default=None)


@router.get('')
async def route(schema: MinerGetAllSchema = Depends()):
    result = await MinerService().get_all(category_id=schema.category_id)
    return result
