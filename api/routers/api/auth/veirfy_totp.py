from datetime import datetime

from fastapi import APIRouter, HTTPException

from api.db.models import User
from api.schemas import UserVerifyTotp
from api.services.base import BaseService
from api.utils import generate_token

router = APIRouter(
    prefix='/verify_totp',
)


@router.post('')
async def route(user_verify_totp: UserVerifyTotp):
    # service = UserService(db)
    # user_candidate:User = await service.get_user(user.email)
    user_candidate = await BaseService().get(User, email=user_verify_totp.email)
    if not user_candidate:
        raise HTTPException(
            status_code=404,
            detail="user not found",
        )
    if user_candidate.last_totp != user_verify_totp.otp or user_candidate.last_totp == 'none':
        raise HTTPException(
            status_code=401,
            detail="wrong code",
        )
    await BaseService().update(user_candidate, last_totp='none')
    if (datetime.now() - user_candidate.totp_sent).days > 0:
        raise HTTPException(
            status_code=401,
            detail='OTP expired',
        )
    token = generate_token(user_verify_totp.email)
    return {
        "token": token,
        "username": user_candidate.email,
        "firstname": user_candidate.firstname,
        "lastname": user_candidate.lastname,
        "id": user_candidate.id,
    }
