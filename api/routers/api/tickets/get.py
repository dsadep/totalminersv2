from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.ticket import TicketService
from api.utils import get_current_user

router = APIRouter(
    prefix='/get',
)


class TicketGetSchema(BaseModel):
    id: int


@router.get('')
async def route(schema: TicketGetSchema = Depends(), user=Depends(get_current_user)):
    result = await TicketService().get(
        user=user,
        id=schema.id,
    )
    return result
