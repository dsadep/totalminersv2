import datetime

from fastapi import APIRouter
from passlib.hash import pbkdf2_sha512
from pydantic import BaseModel

from api.db.models import ResetPasswordRequest
from api.services.base import BaseService

router = APIRouter(
    prefix='/resetPassword',
)


class AuthResetPasswordSchema(BaseModel):
    request_id: str
    new_password: str


@router.post(path='')
async def route(schema: AuthResetPasswordSchema):
    reset_password_request = await BaseService().get(ResetPasswordRequest, id=schema.request_id)
    if not reset_password_request:
        return {
            'status': 'error',
            'description': 'reset_request_not_found',
        }
    if (datetime.datetime.now() - reset_password_request.created_at).days >= 1:
        await BaseService().delete(ResetPasswordRequest, id_=schema.request_id)
        return {
            'status': 'error',
            'description': 'reset_request_expired',
        }
    await BaseService().update(
        reset_password_request.user,
        password=pbkdf2_sha512.hash(schema.new_password),
    )
    return {
        'status': 'ok',
    }
