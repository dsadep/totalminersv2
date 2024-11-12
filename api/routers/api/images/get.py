from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.images import ImageService

router = APIRouter(
    prefix='/get',
)


class ImageGetSchema(BaseModel):
    id: int


@router.get('')
async def route(schema: ImageGetSchema = Depends()):
    result = await ImageService().get(id=schema.id)
    return result
