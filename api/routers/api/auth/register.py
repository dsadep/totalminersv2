from fastapi import APIRouter, HTTPException

from api.db.models import User
from api.schemas import UserRegister
from api.services.base import BaseService
from api.services.headframe import HeadframeService
from api.services.user import UserService

router = APIRouter(
    prefix='/register',
)


@router.post('')
async def route(user: UserRegister):
    reg_result = await UserService().add_new_user(user)
    if not reg_result['result']:
        raise HTTPException(
            status_code=reg_result['status'],
            detail=reg_result['msg'],
        )
    user = await BaseService().get(User, email=user.email)
    await HeadframeService().create_miner_account(user=user)
    return {
        'status': 'ok',
    }
