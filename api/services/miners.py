import datetime
import logging
import math
from typing import Optional

from api.db.models import User, Payment, PaymentTypes, Balance, MinerItem, Worker, MinerItemCategory
from api.modules.headframe import headframe_api
from api.modules.whattomine import what_to_mine_api
from api.services.base import BaseService
from api.services.images import ImageService
from api.services.miners_categories import MinerCategoryService
from api.services.payment import PaymentService
from api.services.settings import SettingsService
from api.services.user import UserService
from api.utils import hash_to_tera_hash, get_hosting_by_hash_rate, value_to_float, hash_to_str
from config import settings


class MinerService:
    model = MinerItem

    async def get(self, id_: int) -> dict:
        miner_item = await BaseService().get(self.model, id=id_, is_hidden=False)
        if not miner_item:
            return {
                'status': 'error',
                'description': f'Miner item #{id_} not found',
            }
        return {
            'status': 'ok',
            'miner_item': await self.generate_miner_item_dict(miner_item=miner_item),
        }

    async def get_all(self, category_id: Optional[int] = None) -> dict:
        if category_id:
            miner_item_category = await BaseService().get(MinerItemCategory, id=category_id)
            if not miner_item_category:
                return {
                    'status': 'error',
                    'description': f'Miner item category #{category_id} not found',
                }
            miners_items = await BaseService().get_all(self.model, category_id=miner_item_category.id, is_hidden=False)
        else:
            miners_items = await BaseService().get_all(self.model, is_hidden=False)
        payback_min = int(await SettingsService().get(key='payback_min', default=0))
        payback_max = int(await SettingsService().get(key='payback_max', default=0))
        return {
            'status': 'ok',
            'miners_items': sorted(
                [
                    await self.generate_miner_item_dict(
                        miner_item=miner_item,
                        payback_min=payback_min,
                        payback_max=payback_max,
                    )
                    for miner_item in miners_items
                ],
                key=lambda x: x['priority'],
                reverse=True,
            ),
        }

    async def get_workers(self, user: User) -> dict:
        workers_db = await BaseService().get_all(Worker, user_id=user.id, hidden=False)
        workers_site = await headframe_api.get_miner_workers(miner_id=user.miner_id)
        workers_statuses = {}
        for worker_site in workers_site.get('data', []):
            workers_statuses[worker_site['id']] = worker_site['status']
        return {
            'status': 'ok',
            'workers': [
                await self.generate_miner_worker_dict(worker=worker, workers_statuses=workers_statuses)
                for worker in workers_db
            ],
        }

    @staticmethod
    async def balance(user: User) -> dict:
        balance = await headframe_api.get_balance(miner_id=user.miner_id)
        btc_price = await headframe_api.get_btc_price()
        value = float(balance['data'][0]['amount'])
        value_usd = round(value * btc_price, 2)
        history = {}
        history_usd = {}
        date_now = datetime.datetime.now()
        for i in range(7):
            date = (date_now - datetime.timedelta(days=i)).strftime(settings.date_format)
            balance_db: Balance = await BaseService().get(Balance, user_id=user.id, date=date)
            balance_value, balance_value_usd = None, None
            if balance_db:
                balance_value = value_to_float(value=balance_db.value, decimal=settings.btc_decimal)
                balance_value_usd = round(balance_value * btc_price, 2)
            history[date] = balance_value
            history_usd[date] = balance_value_usd
        return {
            'status': 'ok',
            'currency': balance['data'][0]['currency'],
            'value': value,
            'value_usd': value_usd,
            'history': history,
            'history_usd': history_usd,
        }

    @staticmethod
    async def information(user: User) -> dict:
        electricity_cost = await SettingsService().get(key='electricity_cost', default=0.06)
        electricity_consumption = await SettingsService().get(key='hash_rate_electricity_consumption', default=15)
        total_earn = await headframe_api.get_miner_total_earn(miner_id=user.miner_id)
        btc_price = await headframe_api.get_btc_price()
        total_earn_currency = total_earn['data'][0]['currency']
        total_earn_value = float(total_earn['data'][0]['amount'])
        total_earn_value_usd = round(total_earn_value * btc_price, 2)
        all_count, online_count = 0, 0
        total_hash_rate, total_energy_consumption = 0, 0
        miner_workers = await headframe_api.get_miner_workers(miner_id=user.miner_id)
        for worker in miner_workers['data']:
            all_count += 1
            logging.critical(type(worker))
            logging.critical(worker)
            logging.critical(type(worker['status']))
            logging.critical(worker['status'])
            logging.critical(worker['status'] == 'stable')
            if worker['status'] == 'stable':
                online_count += 1
                worker_info = await headframe_api.get_worker(worker_id=worker['id'])
                total_hash_rate += round(float(worker_info['1w']['hashrate']), 1)
        total_tera_hash_rate = hash_to_tera_hash(value=total_hash_rate)
        total_energy_consumption = round(total_tera_hash_rate * float(electricity_consumption) / 1_000, 2)
        what_to_mine_data = await what_to_mine_api.get_data(
            hash_rate=total_tera_hash_rate,
            power=total_energy_consumption,
            cost=electricity_cost,
        )
        expected_income = float(what_to_mine_data['revenue'].replace('$', ''))
        expected_income_btc = float(what_to_mine_data['btc_revenue'])
        expected_hosting = await get_hosting_by_hash_rate(
            hash_rate=total_tera_hash_rate,
            electricity_consumption=electricity_consumption,
            electricity_cost=electricity_cost,
        )
        return {
            'status': 'ok',
            'total_earn_currency': total_earn_currency,
            'total_earn_value': total_earn_value,
            'total_earn_value_usd': total_earn_value_usd,
            'online_count': online_count,
            'offline_count': all_count - online_count,
            'total_hash_rate': total_tera_hash_rate,
            'total_energy_consumption': total_energy_consumption,
            'expected_income': expected_income,
            'expected_income_btc': expected_income_btc,
            'expected_hosting': expected_hosting,
            'expected_profit': round(expected_income - expected_hosting, 2),
            'electricity_cost': float(electricity_cost),
        }

    @staticmethod
    async def dashboards(user: User) -> dict:
        btc_price = await headframe_api.get_btc_price()
        dates = []
        payments_data, payments_usd_data = {}, {}
        hash_rate_result, reject_rate_result = {}, {}
        income_result, hosting_result, profit_result = {}, {}, {}
        miners_charts = await headframe_api.get_miners_charts(miner_id=user.miner_id, period='P1W')
        for worker_item_id in miners_charts['data']:
            worker_item = miners_charts['data'][worker_item_id]
            for item in worker_item['points']:
                date = datetime.datetime.fromtimestamp(int(item['timestamp'])).strftime(format='%Y-%m-%d')
                # hash rate
                hash_rate = hash_to_tera_hash(value=float(item['hashrate']))
                if not hash_rate_result.get(date):
                    hash_rate_result[date] = hash_rate
                else:
                    hash_rate_result[date] = (hash_rate_result[date] + hash_rate) / 2
                hash_rate_result[date] = round(hash_rate_result[date], 1)
                # reject rate
                reject_rate = hash_to_tera_hash(value=float(item['rejectrate']))
                reject_rate_result[date] = round(reject_rate_result.get(date, 0) + reject_rate, 2)
                # dates
                dates.append(date)
        for date in dates:
            # payment
            reward_payment = await BaseService().get(Payment, type=PaymentTypes.REWARD, user_id=user.id, date=date)
            reward_payment_value, reward_payment_value_usd = 0, 0
            if reward_payment:
                reward_payment_dict = await PaymentService().generate_payment_dict(
                    payment=reward_payment,
                    btc_price=btc_price,
                )
                reward_payment_value = reward_payment_dict['value']
                reward_payment_value_usd = reward_payment_dict['value_usd']
            payments_data[date] = reward_payment_value
            income_result[date] = reward_payment_value_usd
            # hosting
            hosting_payment = await BaseService().get(Payment, type=PaymentTypes.HOSTING, user_id=user.id, date=date)
            hosting_payment_value_usd = 0
            if hosting_payment:
                hosting_payment_dict = await PaymentService().generate_payment_dict(
                    payment=hosting_payment,
                    btc_price=btc_price,
                )
                hosting_payment_value_usd = -hosting_payment_dict['value_usd']
            hosting_result[date] = hosting_payment_value_usd
            # profit
            profit_value = 0
            if reward_payment_value_usd and hosting_payment_value_usd:
                profit_value = round(reward_payment_value_usd - hosting_payment_value_usd, 2)
            profit_result[date] = profit_value
        return {
            'status': 'ok',
            'payments': payments_data,
            'income': income_result,
            'hosting': hosting_result,
            'profit': profit_result,
            'hash_rate': hash_rate_result,
            'reject_rate': reject_rate_result,
        }

    @staticmethod
    async def generate_miner_item_dict(
            miner_item: MinerItem,
            electricity_cost: float = None,
            payback_min: int = None,
            payback_max: int = None,
    ) -> dict:
        if not miner_item:
            return {}
        if not electricity_cost:
            electricity_cost = float(await SettingsService().get(key='electricity_cost', default=0))
        if not payback_min:
            payback_min = int(await SettingsService().get(key='payback_min', default=0))
        if not payback_max:
            payback_max = int(await SettingsService().get(key='payback_max', default=0))
        what_to_mine_data = await what_to_mine_api.get_data(
            hash_rate=hash_to_tera_hash(value=miner_item.hash_rate),
            power=miner_item.energy_consumption,
            cost=electricity_cost,
        )
        price = value_to_float(value=miner_item.price, decimal=settings.usd_decimal)
        what_to_mine_income = float(what_to_mine_data['revenue'].replace('$', ''))
        what_to_mine_hosting = float(what_to_mine_data['cost'].replace('$', ''))
        what_to_mine_profit = round(what_to_mine_income - what_to_mine_hosting, 2)
        payback = math.ceil(price / (what_to_mine_profit * 30))
        payback_percent = 100 * (payback_min - payback) / (payback_min - payback_max)
        payback_percent = 0 if payback_percent < 0 else payback_percent
        payback_percent = 100 if payback_percent > 100 else payback_percent
        return {
            'id': miner_item.id,
            'name': miner_item.name,
            'description': miner_item.description,
            'category': await MinerCategoryService().generate_miner_item_category_dict(
                miner_item_category=miner_item.category,
            ),
            'hash_rate': miner_item.hash_rate,
            'hash_rate_str': hash_to_str(value=miner_item.hash_rate),
            'energy_consumption': miner_item.energy_consumption,
            'price': price,
            'image': await ImageService().generate_image_dict(image=miner_item.image),
            'income': what_to_mine_income,
            'hosting': what_to_mine_hosting,
            'profit': what_to_mine_profit,
            'priority': miner_item.priority,
            'discount_count': miner_item.discount_count,
            'discount_value': value_to_float(value=miner_item.discount_value, decimal=settings.rub_decimal),
            'payback': payback,
            'payback_percent': round(payback_percent, 2),
            'is_hidden': miner_item.is_hidden,
            'created': miner_item.created.strftime(format=settings.date_time_format),
        }

    async def generate_miner_worker_dict(self, worker: Worker, workers_statuses: dict) -> dict:
        if not worker:
            return {}
        return {
            'id': worker.id,
            'id_str': worker.id_str,
            'name': worker.name,
            'behavior': worker.behavior,
            'user': await UserService.generate_user_dict(user=worker.user),
            'miner_item': await self.generate_miner_item_dict(miner_item=worker.miner_item),
            'status': workers_statuses.get(worker.id_str, 'unavailable'),
            'hidden': worker.hidden,
            'created': worker.created.strftime(format=settings.date_time_format),
        }
