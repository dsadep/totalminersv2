from fastapi import APIRouter, HTTPException, BackgroundTasks

from api.db.models import User
from api.services.base import BaseService
from api.services.user import UserService
from api.utils import send_reset_password_email

router = APIRouter(
    prefix='/requireResetPassword',
)


@router.post(path='')
async def route(email: str, backgroundTasks: BackgroundTasks):
    user = await BaseService().get(User, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    reset_password_request = await UserService().generate_reset_password_request(user.id)
    backgroundTasks.add_task(send_reset_password_email, email=email, code=reset_password_request.id)
    return {
        'status': 'ok',
        'message': 'check email',
    }
