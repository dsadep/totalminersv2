from fastapi import APIRouter
from pydantic import BaseModel

from api.services.feedbacks import FeedbackService

router = APIRouter(
    prefix="/create",
)


class FeedbackCreateSchema(BaseModel):
    name: str
    phone: str


@router.post('')
async def route(schema: FeedbackCreateSchema):
    result = await FeedbackService().create(name=schema.name, phone=schema.phone)
    return result
