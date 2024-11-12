from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User, Billing
from api.services.base import BaseService
from api.services.billings import BillingService
from api.utils import get_current_user

router = APIRouter(
    prefix='/get',
)


class BillingGetSchema(BaseModel):
    id: int


@router.get('')
async def route(schema: BillingGetSchema = Depends(), user: User = Depends(get_current_user)):
    billing = await BaseService().get(Billing, id=schema.id, user_id=user.id)
    if not billing:
        return {
            'status': 'error',
            'description': 'Billing not found'
        }
    return {
        'status': 'ok',
        'data': await BillingService().generate_billing_dict(billing=billing),
    }
