import datetime
import logging

from api.db.models import User, PaymentTypes, Payment, BillingPayment
from api.services.base import BaseService
from config import settings


async def task_hosting_every_month() -> None:
    logging.critical(f'[task_hosting_every_month] start')
    date = datetime.datetime.now()
    if date.day != 1:
        return
    month = date.month - 1
    for user in await BaseService().get_all(User):
        logging.critical(f'[task_hosting_every_month] check user #{user.id}')
        actual_payments = []
        for payment in await BaseService().get_all(Payment, type=PaymentTypes.HOSTING, user_id=user.id):
            payment_date = datetime.datetime.strptime(payment.date, settings.date_format)
            if month != payment_date.month:
                continue
            if await BaseService().get(BillingPayment, payment_id=payment.id):
                continue
            actual_payments.append(payment)
        if not actual_payments:
            continue
        billing = await BaseService().create(Payment, user_id=user.id, type=PaymentTypes.HOSTING)
        payment_value = 0
        for payment in actual_payments:
            await BaseService().create(BillingPayment, billing_id=billing.id, payment_id=payment.id)
            payment_value += payment.value
        await BaseService().update(billing, value=payment_value)
    logging.critical('[task_hosting_every_month] END')
