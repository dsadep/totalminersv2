from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.billings import BillingService
from api.utils import get_current_user

router = APIRouter(
    prefix='/payment/type',
)


class BillingUpdatePaymentTypeSchema(BaseModel):
    id: int
    payment_type:str


@router.get('')
async def route(schema: BillingUpdatePaymentTypeSchema = Depends(), user: User = Depends(get_current_user)):
    result = await BillingService().update_payment_type(user=user, id=schema.id, payment_type=schema.payment_type)
    return result
