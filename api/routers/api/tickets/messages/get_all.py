from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.messages import MessageService
from api.utils import get_current_user

router = APIRouter(
    prefix="/get/all",
)


class TicketMessageGetAllSchema(BaseModel):
    ticket_id: int


@router.post('')
async def route(schema: TicketMessageGetAllSchema, user=Depends(get_current_user)):
    result = await MessageService().get_all(user=user, ticket_id=schema.ticket_id)
    return result
