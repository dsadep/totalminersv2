import asyncio
import logging

from api.db.models import Billing, BillingStates, BillingPaymentTypes
from api.services.base import BaseService
from api.tasks.billings.utils import payment_check_btc, payment_check_usdt


async def function() -> None:
    for billing in await BaseService().get_all(Billing, state=BillingStates.CONFIRMATION):
        if billing.payment_type not in [BillingPaymentTypes.BTC, BillingPaymentTypes.USDT]:
            continue
        logging.critical(f'[task_billing_payment_check] check billing #{billing.id}')
        if billing.payment_type == BillingPaymentTypes.RUS_CARD:
            continue
        elif billing.payment_type == BillingPaymentTypes.BTC:
            if not await payment_check_btc(billing=billing):
                continue
        elif billing.payment_type == BillingPaymentTypes.USDT:
            if not await payment_check_usdt(billing=billing):
                continue
        await BaseService().update(billing, state=BillingStates.COMPLETED)


async def task_billing_payment_check():
    logging.critical(f'[task_billing_payment_check] start')
    while True:
        try:
            await function()
            await asyncio.sleep(30)
        except Exception as e:
            logging.critical(f'Exception \n {e}')
