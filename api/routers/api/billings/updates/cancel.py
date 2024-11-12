from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.billings import BillingService
from api.utils import get_current_user

router = APIRouter(
    prefix='/cancel',
)


class BillingUpdateCancelSchema(BaseModel):
    id: int


@router.get('')
async def route(schema: BillingUpdateCancelSchema = Depends(), user: User = Depends(get_current_user)):
    result = await BillingService().update_cancel(user=user, id=schema.id)
    return result
