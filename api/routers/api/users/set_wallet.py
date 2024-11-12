from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.user import UserService
from api.utils import get_current_user

router = APIRouter(
    prefix='/setWallet',
)


class UpdateUserWalletSchema(BaseModel):
    wallet: str
    otp: str


@router.post(path='')
async def route(schema: UpdateUserWalletSchema, user: User = Depends(get_current_user)):
    result = await UserService().update_wallet(
        user=user,
        wallet=schema.wallet,
        otp=schema.otp,
    )
    return result
