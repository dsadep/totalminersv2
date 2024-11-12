import logging

import aiohttp

from api.db.models import Billing
from api.services.billings import BillingService
from api.services.settings import SettingsService
from api.utils import value_to_float
from config import settings


async def payment_check_btc(billing: Billing) -> bool:
    try:
        btc_wallet = await SettingsService().get(key='payment_btc')
        billing_values = await BillingService.get_values(billing=billing)
        billing_value = billing_values['value']
        billing_hash = billing.payment_data
        url = f"https://blockchain.info/rawtx/{billing_hash}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                json_data = await response.json()
        if json_data.get('error'):
            logging.critical(f'[payment_check_btc] billing #{billing.id} | {json_data}')
            return False
        total_amount_input = 0
        for input_ in json_data['inputs']:
            total_amount_input += float(input_['prev_out']['value'])
        total_amount_input = value_to_float(value=total_amount_input, decimal=settings.btc_decimal)  # float
        wallet_address = None
        total_amount_output = 0
        for output in json_data['out']:
            if not output.get('addr'):
                continue
            total_amount_output += float(output['value'])
            wallet_address = output['addr']
        total_amount_output = value_to_float(value=total_amount_output, decimal=settings.btc_decimal)  # float
        if wallet_address != btc_wallet:
            logging.critical(f'[payment_check_btc] billing #{billing.id} | {wallet_address} != {btc_wallet}')
            return False
        if (total_amount_input - total_amount_output) < 0:
            logging.critical(f'[payment_check_btc] billing #{billing.id} | {total_amount_input - total_amount_output}')
            return False
        if total_amount_output < billing_value:
            logging.critical(f'[payment_check_btc] billing #{billing.id} | {total_amount_output} < {billing_value}')
            return False
        logging.critical(f'[payment_check_btc] billing #{billing.id} | TRUE')
        return True
    except Exception as e:
        logging.critical(f'[payment_check_btc] billing #{billing.id} | {e}')
        return False


async def payment_check_usdt(billing: Billing) -> bool:
    try:
        usdt_wallet = await SettingsService().get(key='payment_usdt')
        billing_values = await BillingService.get_values(billing=billing)
        billing_value = billing_values['value']
        billing_hash = billing.payment_data
        url = f'https://apilist.tronscanapi.com/api/transaction-info?hash={billing_hash}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                json_data = await response.json()
        if not json_data:
            logging.critical(f'[payment_check_usdt] billing #{billing.id} | {json_data}')
            return False
        total_amount_output = value_to_float(value=json_data['transfersAllList'][0]['amount_str'], decimal=6)
        wallet_address = json_data['transfersAllList'][0]['to_address']
        info_cash_success = json_data['contractRet']
        info_cash_success2 = json_data['confirmed']
        if wallet_address != usdt_wallet:
            logging.critical(f'[payment_check_usdt] billing #{billing.id} | {wallet_address} != {usdt_wallet}')
            return False
        if total_amount_output < billing_value:
            logging.critical(f'[payment_check_usdt] billing #{billing.id} | {total_amount_output} < {billing_value}')
            return False
        if info_cash_success != 'SUCCESS':
            logging.critical(f'[payment_check_usdt] billing #{billing.id} | {info_cash_success}')
            return False
        if not info_cash_success2:
            logging.critical(f'[payment_check_usdt] billing #{billing.id} | {info_cash_success2}')
            return False
        logging.critical(f'[payment_check_usdt] billing #{billing.id} | TRUE')
        return True
    except Exception as e:
        logging.critical(f'[payment_check_usdt] billing #{billing.id} | {e}')
        return False
