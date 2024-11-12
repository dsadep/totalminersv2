import datetime
import logging

from api.db.models import User, PaymentTypes, PaymentSite, Payment, PaymentCurrencies
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.utils import value_to_int
from config import settings


async def task_payment_every_day() -> None:
    logging.critical(f'[task_payment_every_day] start')
    for user in await BaseService().get_all(User):
        logging.critical(f'[task_payment_every_day] check user #{user.id}')
        payments_sites = await headframe_api.get_miner_payments(miner_id=user.miner_id, limit=7)
        logging.critical(payments_sites)
        for payment_site in payments_sites['data']:
            if await BaseService().get(PaymentSite, site_id=payment_site['id']):
                continue
            payment_type = None
            extra = {}
            payment_value = float(payment_site['amount'])
            if payment_site['type'] == 'reward':
                payment_type = PaymentTypes.REWARD
                extra['hash_rate'] = int(payment_site['metadata']['hashrate'])
            elif payment_site['type'] == 'payout':
                payment_type = PaymentTypes.PAYOUT
                payment_value = -payment_value
            payment = await BaseService().create(
                Payment,
                type=payment_type,
                currency=PaymentCurrencies.BTC,
                user_id=user.id,
                value=value_to_int(value=payment_value, decimal=settings.btc_decimal),
                date=payment_site['created_at'].split('T')[0],
                date_time=datetime.datetime.fromisoformat(payment_site['created_at'].rstrip("Z")),
            )
            await BaseService().create(
                PaymentSite,
                payment_id=payment.id,
                site_id=payment_site['id'],
                **extra,
            )
    logging.critical('[task_payment_every_day] END')
