from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.db.models import User
from api.services.user import UserService
from api.utils import get_current_user

router = APIRouter(
    prefix='/update/password',
)


class UserUpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    otp: str


@router.post(path='')
async def route(schema: UserUpdatePasswordSchema, user: User = Depends(get_current_user)):
    result = await UserService().update_password(
        user=user,
        old_password=schema.old_password,
        new_password=schema.new_password,
        otp=schema.otp,
    )
    return result
