from typing import Optional
from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel

from api.services.messages import MessageService
from api.services.images import ImageService
from api.utils import get_current_user

router = APIRouter(
    prefix="/create",
)


class TicketMessageCreateSchema(BaseModel):
    ticket_id: int
    text: str
    file: Optional[UploadFile]


@router.post('')
async def route(schema: TicketMessageCreateSchema, user=Depends(get_current_user)):
    if schema.file:
        image = await ImageService().create(file=schema.file)
        result = await MessageService().create(user=user, ticket_id=schema.ticket_id, content=schema.text, image_id=image['image_id'])
    else:
        result = await MessageService().create(user=user, ticket_id=schema.ticket_id, content=schema.text)
    return result
