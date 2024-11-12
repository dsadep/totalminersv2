import pyotp
from fastapi import APIRouter, Depends, HTTPException

from api.db.models import User
from api.services.base import BaseService
from api.utils import get_current_user

router = APIRouter(
    prefix="/enablemfa",
)


@router.post('')
async def route(otp: str, user: User = Depends(get_current_user)):
    if user.mfa_enabled:
        raise HTTPException(
            status_code=400,
            detail='MFA already enabled',
        )
    totp_auth = pyotp.TOTP(user.mfa_key)
    if not otp == totp_auth.now():
        raise HTTPException(
            status_code=401,
            detail='wrong code',
        )
    await BaseService().update(user, mfa_enabled=True)
    return {
        'message': 'ok',
    }
