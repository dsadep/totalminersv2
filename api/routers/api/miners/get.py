from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.miners import MinerService

router = APIRouter(
    prefix='/get',
)


class MinerGetSchema(BaseModel):
    id: int


@router.get('')
async def route(schema: MinerGetSchema = Depends()):
    result = await MinerService().get(id_=schema.id)
    return result
