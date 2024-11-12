from fastapi import APIRouter, Depends, UploadFile

from api.db.models import User
from api.services.user import UserService
from api.utils import get_current_user

router = APIRouter(
    prefix='/update/image',
)


@router.post(path='')
async def route(file: UploadFile, user: User = Depends(get_current_user)):
    result = await UserService().update_image(user=user, file=file)
    return result
