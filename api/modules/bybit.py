import asyncio

import aiohttp

VALUES_LIST = [
    # 50_000,
    100_000,
    # 150_000,
]
PAYMENT_IDS_LIST = [
    # 382,  # SBP
    581,  # T-BANK
    # 595,  # SBERBANK,
]


async def get_bybit_rub():
    rates = []
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url='https://api2.bybit.com/fiat/otc/item/online',
            json={
                'userId': '',
                'tokenId': 'USDT',
                'currencyId': 'RUB',
                # 'side': '0',  # Покупка
                'side': '1',  # Продажа
                'payment': [str(581)],
                'size': '5',
                'page': '1',
                'amount': str(100_000),
                'authMaker': True,
            },
        )
        response_json = await response.json()
        rates += [float(item['price']) for item in response_json['result']['items']]
    if not rates:
        return
    rate_value = sum(rates) / len(rates)
    return rate_value

