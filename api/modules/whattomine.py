import json
import logging

import aiohttp


class WhatToMineApi:
    """
    GET
    """

    async def request_get(self, url: str):
        async with aiohttp.ClientSession() as session:
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
        async with aiohttp.ClientSession() as session:
            return await self.request_post_with_session(session=session, url=url, data=data)

    @staticmethod
    async def request_post_with_session(session: aiohttp.ClientSession, url: str, data: dict):
        async with session.post(url=url, data=data) as response:
            json_data = await response.json()
        logging.critical(f'POST {url} | {json.dumps(json_data)}')
        return json_data

    """
    API
    """

    async def get_data(self, hash_rate: float, power: float, cost: float ) -> tuple[float, float]:
        url = 'https://whattomine.com/coins/1.json?'
        url += f'hr={hash_rate}&p={power}&fee=0.0&cost={cost}&cost_currency=USD&hcost=0.0&span_br=1h&span_d=1h'
        return await self.request_get(url=url)


what_to_mine_api = WhatToMineApi()
