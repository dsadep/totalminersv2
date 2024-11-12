from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.user import UserService
from api.utils import get_current_user

router = APIRouter(
    prefix='/wallet/delete',
)


class UserWalletDeleteSchema(BaseModel):
    otp: str


@router.post(path='')
async def route(schema: UserWalletDeleteSchema, user: User = Depends(get_current_user)):
    result = await UserService().delete_wallet(user=user, otp=schema.otp)
    return result
