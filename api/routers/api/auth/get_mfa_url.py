import pyotp
from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import pbkdf2_sha512

from api.db.models import User
from api.services.base import BaseService
from api.utils import get_current_user

router = APIRouter(
    prefix="/getmfa",
)


@router.get('')
async def route(password: str, user: User = Depends(get_current_user)):
    if not user.mfa_key:
        await BaseService().update(user, mfa_key=pyotp.random_base32())
    if not pbkdf2_sha512.verify(password, user.password):
        raise HTTPException(
            status_code=401,
            detail='wrong password',
        )

    totp_auth = pyotp.totp.TOTP(user.mfa_key).provisioning_uri(name=user.email, issuer_name='TotalMiners')
    return {
        'status': 'ok',
        'mfa_url': totp_auth,
    }
