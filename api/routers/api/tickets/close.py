from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.ticket import TicketService
from api.utils import get_current_user

router = APIRouter(
    prefix="/close",
)


class TicketCloseSchema(BaseModel):
    id: int


@router.post('')
async def route(schema: TicketCloseSchema, user=Depends(get_current_user)):
    result = await TicketService().close(user=user, id=schema.id)
    return result
