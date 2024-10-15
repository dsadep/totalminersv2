from fastapi import APIRouter, Depends, UploadFile
from typing import Optional
from pydantic import BaseModel

from api.services.ticket import TicketService
from api.utils import get_current_user

router = APIRouter(
    prefix="/create",
)


class TicketCreateSchema(BaseModel):
    title: str
    text: str
    file: Optional[UploadFile]

@router.post('')
async def route(schema: TicketCreateSchema, user=Depends(get_current_user)):
    result = await TicketService().create(user=user, title=schema.title, content=schema.text, file=schema.file)
    return result
