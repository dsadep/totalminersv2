from fastapi import APIRouter, Depends

from api.db.models import User
from api.utils import get_current_user

router = APIRouter(
    prefix="/validate",
)


@router.post('')
async def route(user: User = Depends(get_current_user)):
    return {
        'message': 'ok',
    }
