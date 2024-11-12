from fastapi import APIRouter, Depends

from api.services.ticket import TicketService
from api.utils import get_current_user

router = APIRouter(
    prefix='/get/all',
)


@router.get('')
async def route(user=Depends(get_current_user)):
    result = await TicketService().get_all(user=user)
    return result
