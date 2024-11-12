from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.images import ImageService

router = APIRouter(
    prefix='/delete',
)


class ImageDeleteSchema(BaseModel):
    id: int


@router.get('')
async def route(schema: ImageDeleteSchema = Depends()):
    result = await ImageService().delete(id=schema.id)
    return result
