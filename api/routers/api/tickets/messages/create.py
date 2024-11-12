from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.messages import MessageService
from api.utils import get_current_user

router = APIRouter(
    prefix="/create",
)


class TicketMessageCreateSchema(BaseModel):
    ticket_id: int
    text: str


@router.post('')
async def route(schema: TicketMessageCreateSchema, user=Depends(get_current_user)):
    result = await MessageService().create(user=user, ticket_id=schema.ticket_id, content=schema.text)
    return result
