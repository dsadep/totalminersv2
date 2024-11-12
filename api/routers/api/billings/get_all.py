from fastapi import APIRouter, Depends

from api.db.models import User, Billing
from api.services.base import BaseService
from api.services.billings import BillingService
from api.utils import get_current_user

router = APIRouter(
    prefix='/get/all',
)


@router.get('')
async def route(user: User = Depends(get_current_user)):
    billings = await BaseService().get_all(Billing, user_id=user.id)
    return {
        'status': 'ok',
        'data': [
            await BillingService().generate_billing_dict(billing=billing)
            for billing in billings
        ],
    }
