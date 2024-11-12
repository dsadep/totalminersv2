from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.billings import BillingService
from api.utils import get_current_user

router = APIRouter(
    prefix='/complete',
)


class BillingUpdateCompleteSchema(BaseModel):
    id: int
    data: str


@router.get('')
async def route(schema: BillingUpdateCompleteSchema = Depends(), user: User = Depends(get_current_user)):
    result = await BillingService().update_complete(user=user, id=schema.id, data=schema.data)
    return result
