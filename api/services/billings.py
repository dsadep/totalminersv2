from sqlalchemy.sql.operators import or_

from api.db.models import Billing, BillingPaymentTypes, User, BillingStates, BillingTypes
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.services.images import ImageService
from api.services.settings import SettingsService
from api.utils import value_to_float
from config import settings


class BillingService:
    model = Billing

    async def update_payment_type(
            self,
            user: User,
            id: int,
            payment_type: str,
    ):
        billing = await BaseService().get(self.model, user_id=user.id, id=id)
        await BaseService().update(billing, payment_type=payment_type)
        return {
            'status': 'ok',
            'billing': await self.generate_billing_dict(billing=billing)
        }

    async def update_complete(
            self,
            user: User,
            id: int,
            data: str,
    ):
        billing = await BaseService().get(self.model, user_id=user.id, id=id)
        await BaseService().update(billing, payment_data=data, state=BillingStates.CONFIRMATION)
        return {
            'status': 'ok',
            'billing': await self.generate_billing_dict(billing=billing)
        }

    async def update_cancel(
            self,
            user: User,
            id: int,
    ):
        billing = await BaseService().get(self.model, user_id=user.id, id=id)
        if billing.type == BillingTypes.HOSTING:
            return {
                'status': 'error',
                'description': f'Billing for type {billing.type} not be cancel'
            }
        await BaseService().update(billing, state=BillingStates.CANCELED)
        return {
            'status': 'ok',
            'billing': await self.generate_billing_dict(billing=billing)
        }

    @staticmethod
    async def generate_billing_dict(billing: Billing) -> dict:
        payment_detail = None
        decimal = settings.usd_decimal
        if billing.payment_type == BillingPaymentTypes.RUS_CARD:
            payment_detail = await SettingsService().get(key='payment_bank_card')
            decimal = settings.rub_decimal
        elif billing.payment_type == BillingPaymentTypes.BTC:
            payment_detail = await SettingsService().get(key='payment_btc')
            decimal = settings.btc_decimal
        elif billing.payment_type == BillingPaymentTypes.USDT:
            payment_detail = await SettingsService().get(key='payment_usdt')
            decimal = settings.usd_decimal
        return {
            'id': billing.id,
            'user_id': billing.user_id,
            'type': billing.type,
            'currency': billing.currency.upper(),
            'payment_type': billing.payment_type,
            'payment_detail': payment_detail,
            'payment_data': billing.payment_data,
            'state': billing.state,
            'value': value_to_float(value=billing.value, decimal=decimal),
            'value_usd': value_to_float(value=billing.value_usd, decimal=settings.usd_decimal),
            'image': await ImageService().generate_image_dict(image=billing.image),
            'date': billing.created.strftime('%d.%m.%Y'),
            'time': billing.created.strftime('%H:%M'),
            'created': billing.created.strftime(format=settings.date_time_format)
        }

    async def active_billings_count(self, user: User) -> int:
        custom_where = or_(self.model.state == BillingStates.INVOICED, self.model.state == BillingStates.WAITING)
        billings = await BaseService().get_list(self.model, custom_where=custom_where, user_id=user.id)
        return len(billings)

    async def active_billings(self, user: User) -> bool:
        custom_where = or_(self.model.state == BillingStates.INVOICED, self.model.state == BillingStates.WAITING)
        billings = await BaseService().get_list(self.model, custom_where=custom_where, user_id=user.id)
        return bool(billings)

    @staticmethod
    async def get_values(billing: Billing) -> dict:
        currency = 'USD'
        value = value_usd = value_to_float(value=billing.value, decimal=settings.usd_decimal)
        if billing.payment_type == BillingPaymentTypes.BTC:
            currency = 'BTC'
            btc_price = await headframe_api.get_btc_price()
            value = value_to_float(value=billing.value, decimal=settings.btc_decimal)
            value_usd = round(value * btc_price, 2)
        return {
            'currency': currency,
            'value': value,
            'value_usd': value_usd,
        }
