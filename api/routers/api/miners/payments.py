import logging
from math import ceil

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.db.models import Payment
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.services.payment import PaymentService
from api.utils import get_current_user

router = APIRouter(
    prefix='/payments',
)


class MinerPaymentSchema(BaseModel):
    limit: int = 0
    page: int = 1


@router.get('')
async def route(schema: MinerPaymentSchema = Depends(), user=Depends(get_current_user)):
    btc_price = await headframe_api.get_btc_price()
    payments, results = await BaseService().search(Payment, limit=schema.limit, page=schema.page, user_id=user.id)
    payments = [
        await PaymentService().generate_payment_dict(payment=payment, btc_price=btc_price)
        for payment in payments
    ]
    payments = sorted(payments, key=lambda x: x['date_time'])[::-1]
    pages = 1
    if schema.limit:
        pages = ceil(results / schema.limit)
    return {
        'status': 'ok',
        'data': payments,
        'results': results,
        'page': schema.page,
        'pages': pages,
    }
