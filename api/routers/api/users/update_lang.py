from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.user import UserService
from api.utils import get_current_user

router = APIRouter(
    prefix='/update/lang',
)


class UserUpdateLangSchema(BaseModel):
    lang: str


@router.post(path='')
async def route(schema: UserUpdateLangSchema, user: User = Depends(get_current_user)):
    result = await UserService().update_lang(user=user, lang=schema.lang.lower())
    return result
