from fastapi import APIRouter, UploadFile, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.images import ImageService
from api.utils import get_current_user

router = APIRouter(
    prefix='/create',
)


class ImageDeleteSchema(BaseModel):
    id: int


@router.post('')
async def route(file: UploadFile, user: User = Depends(get_current_user)):
    result = await ImageService().create(file=file)
    return result
