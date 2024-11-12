import json
import logging

import aiohttp

from config import settings


class HeadframeApi:
    url_base: str = 'https://pool.headframe.io/api'
    url: str = f'{url_base}/backend/v0.1'
    token: str
    cookie: dict

    def __init__(self, token: str):
        self.token = token
        self.cookie = {
            'ory_session_relaxedwescoffeywmz1r7og': self.token,
        }

    """
    GET
    """

    async def request_get(self, url: str):
        async with aiohttp.ClientSession(cookies=self.cookie) as session:
            return await self.request_get_with_session(session=session, url=url)

    @staticmethod
    async def request_get_with_session(session: aiohttp.ClientSession, url: str):
        async with session.get(url=url) as response:
            json_data = await response.json()
        logging.critical(f'GET {url} | {json.dumps(json_data)}')
        return json_data

    """
    POST
    """

    async def request_post(self, url: str, data: dict):
        async with aiohttp.ClientSession(cookies=self.cookie) as session:
            return await self.request_post_with_session(session=session, url=url, data=data)

    @staticmethod
    async def request_post_with_session(session: aiohttp.ClientSession, url: str, data: dict):
        async with session.post(url=url, data=data) as response:
            json_data = await response.json()
        logging.critical(f'POST {url} | {data} | {json.dumps(json_data)}')
        return json_data

    """
    API
    """

    async def get_balance(self, miner_id: str) -> dict:
        url = f'{self.url}/miners/{miner_id}/balance'
        return await self.request_get(url=url)

    async def get_miner_total_earn(self, miner_id: str) -> dict:
        url = f'{self.url}/miners/{miner_id}/earned-all-time'
        return await self.request_get(url=url)

    async def update_wallet(self, wallet_id: str, wallet: str) -> dict:
        url = f'{self.url}/wallets/{wallet_id}/addresses'
        return await self.request_post(url=url, data={'address': wallet})

    async def get_miners_charts(self, miner_id: str, period: str = 'P1W') -> dict:
        url = f'{self.url}/miners/charts?period={period}&id={miner_id}'
        return await self.request_get(url=url)

    async def get_miner_payments(self, miner_id: str, limit: int = 10) -> dict:
        url = f'{self.url}/miners/{miner_id}/payments?limit={limit}'
        return await self.request_get(url=url)

    async def get_miner_workers(self, miner_id: str) -> dict:
        url = f'{self.url}/miners/{miner_id}/workers?limit=100'
        return await self.request_get(url=url)

    """
    API PLUS
    """

    async def get_worker(self, worker_id: str) -> dict:
        url = f'{self.url}/workers/stats?id={worker_id}'
        result = await self.request_get(url=url)
        return result[worker_id]

    async def get_btc_price(self) -> float:
        url = f'{self.url_base}/binance?symbol=BTCUSDT'
        result = await self.request_get(url=url)
        return float(result['price'])


headframe_api = HeadframeApi(token=settings.token)
