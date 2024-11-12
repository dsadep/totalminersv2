from fastapi import APIRouter, Depends

from api.db.models import User
from api.services.user import UserService
from api.utils import get_current_user

router = APIRouter(
    prefix='/{id:int}',
)


@router.get(path='')
async def route(id: int, user: User = Depends(get_current_user)):
    result = await UserService().get(user=user, id=id)
    return result
