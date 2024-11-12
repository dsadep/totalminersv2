from fastapi import APIRouter, Depends
from pydantic import BaseModel, model_validator

from api.db.models import User, BillingPaymentTypes
from api.services.market import MarketService
from api.utils import get_current_user

router = APIRouter(
    prefix='/buy',
)


class MarketCartBuySchema(BaseModel):
    payment_type: str

    @model_validator(mode='after')
    def check_type(self) -> 'MarketCartBuySchema':
        payments_types = [BillingPaymentTypes.RUS_CARD, BillingPaymentTypes.BTC, BillingPaymentTypes.USDT]
        if self.payment_type not in payments_types:
            raise ValueError(f'Payment type must be {payments_types}')
        return self


@router.get('')
async def route(schema: MarketCartBuySchema = Depends(), user: User = Depends(get_current_user)):
    result = await MarketService().cart_buy(user=user, payment_type=schema.payment_type)
    return result
