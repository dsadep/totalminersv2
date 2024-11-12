import asyncio
import datetime
import logging

from api.db.models import User, Balance
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.utils import value_to_int
from config import settings


async def function() -> None:
    date = datetime.datetime.now().strftime(format=settings.date_format)
    for user in await BaseService().get_all(User):
        logging.critical(f'[task_balance_save] check user #{user.id}')
        balance = await headframe_api.get_balance(miner_id=user.miner_id)
        if not balance:
            continue
        balance_value = float(balance['data'][0]['amount'])
        await BaseService().create(
            Balance,
            user_id=user.id,
            value=value_to_int(value=balance_value, decimal=settings.btc_decimal),
            date=date,
        )


async def task_balance_save():
    logging.critical(f'[task_balance_save] start')
    while True:
        try:
            await function()
        except Exception as e:
            logging.critical(f'Exception \n {e}')
        await asyncio.sleep(6 * 60 * 60)
