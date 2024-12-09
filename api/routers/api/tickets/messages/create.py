from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
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

@router.post('')
async def route(schema: TicketMessageCreateSchema, file: Optional[UploadFile] = File(None), user=Depends(get_current_user)):
    if file:
        image = await ImageService().create(file=file)
        result = await MessageService().create(user=user, ticket_id=schema.ticket_id, content=schema.text, image_id=image['image_id'])
    else:
        result = await MessageService().create(user=user, ticket_id=schema.ticket_id, content=schema.text)
    return result
