import pyotp
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.base import BaseService
from api.utils import get_current_user

router = APIRouter(
    prefix="/mfa/disable",
)


class AuthDisableMfaSchema(BaseModel):
    code: str


@router.post('')
async def route(schema: AuthDisableMfaSchema, user: User = Depends(get_current_user)):
    if not user.mfa_enabled:
        return {
            'status': 'error',
            'description': 'MFA already disabled'
        }
    totp_auth = pyotp.TOTP(user.mfa_key)
    if not schema.code == totp_auth.now():
        return {
            'status': 'error',
            'description': 'Wrong mfa code'
        }
    await BaseService().update(user, mfa_enabled=False)
    return {
        'status': 'ok',
    }
