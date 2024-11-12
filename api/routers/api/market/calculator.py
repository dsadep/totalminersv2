import aiohttp
from fastapi import APIRouter

from api.services.settings import SettingsService

router = APIRouter(
    prefix='/calculator',
)


@router.get('')
async def route():
    invest_min = await SettingsService().get(key='invest_min', default=5400)
    invest_max = await SettingsService().get(key='invest_max', default=300000)
    electricity_cost = await SettingsService().get(key='electricity_cost', default=0.06)
    hash_rate_electricity_consumption = await SettingsService().get(key='hash_rate_electricity_consumption', default=15)
    hash_rate_cost = await SettingsService().get(key='hash_rate_cost', default=20)
    url = (
        f'https://whattomine.com/coins/1.json?'
        f'hr=234&p=3600.0&fee=0.0&cost={electricity_cost}&cost_currency=USD&hcost=0.0&span_br=24h'
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return {
        'difficulty': data['difficulty'],
        'reward': data['block_reward'],
        'btc_price': data['exchange_rate'],
        'invest_min': float(invest_min),
        'invest_max': float(invest_max),
        'electricity_cost': float(electricity_cost),
        'hash_rate_electricity_consumption': float(hash_rate_electricity_consumption),
        'hash_rate_cost': float(hash_rate_cost),
    }
