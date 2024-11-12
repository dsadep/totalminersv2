import datetime
import logging

from api.db.models import User, PaymentTypes, Payment, PaymentCurrencies
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.services.settings import SettingsService
from api.utils import hash_to_tera_hash, value_to_int, get_hosting_by_hash_rate
from config import settings


async def task_hosting_every_day() -> None:
    logging.critical(f'[task_hosting_every_day] start')
    electricity_consumption = await SettingsService().get(key='hash_rate_electricity_consumption', default=15)
    electricity_cost = await SettingsService().get(key='electricity_cost', default=0.06)
    for user in await BaseService().get_all(User):
        logging.critical(f'[task_hosting_every_day] check user #{user.id}')
        hash_rate_list = {}
        miners_charts = await headframe_api.get_miners_charts(miner_id=user.miner_id, period='P1W')
        for worker_item_id in miners_charts['data']:
            worker_item = miners_charts['data'][worker_item_id]
            for item in worker_item['points']:
                date = datetime.datetime.fromtimestamp(int(item['timestamp'])).strftime(format=settings.date_format)
                hash_rate_ = hash_to_tera_hash(value=float(item['hashrate']))
                if not hash_rate_list.get(date):
                    hash_rate_list[date] = []
                hash_rate_list[date].append(hash_rate_)
        for date, items in hash_rate_list.items():
            if len(items) < 6:
                continue
            if await BaseService().get(Payment, type=PaymentTypes.HOSTING, user_id=user.id, date=date):
                continue
            hash_rate_item = round(sum(items) / len(items), 1)
            hosting_item = await get_hosting_by_hash_rate(
                hash_rate=hash_rate_item,
                electricity_consumption=electricity_consumption,
                electricity_cost=electricity_cost,
            )
            if hosting_item == 0:
                continue
            await BaseService().create(
                Payment,
                type=PaymentTypes.HOSTING,
                currency=PaymentCurrencies.USD,
                user_id=user.id,
                date=date,
                value=-value_to_int(value=hosting_item, decimal=settings.usd_decimal),
            )
    logging.critical('[task_hosting_every_day] END')
