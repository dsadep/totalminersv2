from api.db.models import Payment, PaymentCurrencies, PaymentTypes, PaymentSite
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.utils import value_to_float, hash_to_tera_hash
from config import settings


class PaymentService:
    model = Payment

    @staticmethod
    async def generate_payment_dict(payment: Payment, btc_price: float = None):
        if not payment:
            return {}
        value = value_usd = 0
        if payment.currency == PaymentCurrencies.USD:
            value = value_usd = value_to_float(value=payment.value, decimal=settings.usd_decimal)
        elif payment.currency == PaymentCurrencies.BTC:
            if not btc_price:
                btc_price = await headframe_api.get_btc_price()
            value = value_to_float(value=payment.value, decimal=settings.btc_decimal)
            value_usd = round(value * btc_price, 2)
        extra = {}
        if payment.type == PaymentTypes.REWARD:
            payment_site = await BaseService().get(PaymentSite, payment_id=payment.id)
            extra['hash_rate'] = hash_to_tera_hash(value=payment_site.hash_rate)
        return {
            'id': payment.id,
            'type': payment.type,
            'currency': payment.currency,
            'user_id': payment.user_id,
            'value': value,
            'value_usd': value_usd,
            'date': payment.date_time.strftime("%d.%m.%Y"),
            'time': payment.date_time.strftime("%H:%M"),
            'date_time': payment.date_time,
            'created': payment.created.strftime("%d.%m.%Y %H:%M"),
            **extra,
        }
