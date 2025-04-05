from datetime import datetime
from fastapi import APIRouter, Depends

from api.services.ticket import TicketService
from api.utils import get_current_user

router = APIRouter(
    prefix="/get/sorted"
)

# @router.get("/status")
# async def tickets_sorted_by_status(is_open: bool, user=Depends(get_current_user)):
#     result = await TicketService().sort_by_status(user=user, status=is_open)
#     return result

# @router.get("/date")
# async def tickets_sorted_by_date(created_at: datetime, user=Depends(get_current_user)):
#     result = await TicketService().sort_by_date(user=user, created_at=created_at)
#     return result