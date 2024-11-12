import logging

from api.db.models import MinerItem, User, BuyRequest, BuyRequestMinerItem, Billing, \
    BillingTypes, BillingBuyRequest, BillingStates, MarketCart, BillingPaymentTypes, BillingCurrencies
from api.modules.bybit import get_bybit_rub
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.services.billings import BillingService
from api.services.miners import MinerService
from api.services.settings import SettingsService
from api.utils import value_to_float, value_to_int
from config import settings


class MarketService:
    cart_model = MarketCart

    async def cart_set(self, user: User, miner_item_id: int, count: int) -> dict:
        miner_item = await BaseService().get(MinerItem, id=miner_item_id)
        if not miner_item:
            return {
                'status': 'error',
                'description': 'Miner item not found',
            }
        market_cart = await BaseService().get(self.cart_model, user_id=user.id, miner_item_id=miner_item.id)
        if count <= 0:
            if market_cart:
                await BaseService().delete(self.cart_model, id_=market_cart.id)
        else:
            if not market_cart:
                await BaseService().create(self.cart_model, user_id=user.id, miner_item_id=miner_item.id, count=count)
            else:
                await BaseService().update(market_cart, count=count)
        return await self.cart_get(user=user)

    async def cart_get(self, user: User) -> dict:
        markets_carts = await BaseService().get_all(self.cart_model, user_id=user.id)
        payback_min = int(await SettingsService().get(key='payback_min', default=0))
        payback_max = int(await SettingsService().get(key='payback_max', default=0))
        data = []
        discount = 0
        count = 0
        summary = 0
        for market_cart in markets_carts:
            data.append({
                **await MinerService().generate_miner_item_dict(
                    miner_item=market_cart.miner_item,
                    payback_min=payback_min,
                    payback_max=payback_max,
                ),
                'count': market_cart.count,
            })
            miner_sum = market_cart.miner_item.price * market_cart.count
            if market_cart.count >= market_cart.miner_item.discount_count:
                discount_value = value_to_float(
                    value=market_cart.miner_item.discount_value,
                    decimal=settings.rate_decimal,
                )
                discount += miner_sum * (discount_value / 100)
            count += market_cart.count
            summary += miner_sum
        summary = value_to_float(value=summary, decimal=settings.usd_decimal, round_value=2)
        discount = value_to_float(value=discount, decimal=settings.usd_decimal, round_value=2)
        return {
            'status': 'ok',
            'data': data,
            'count': count,
            'summary_raw': summary,
            'summary': round(summary - discount, 2),
            'discount': discount,
            'billing_count': await BillingService().active_billings_count(user=user),
        }

    async def cart_buy(self, user: User, payment_type: str) -> dict:
        print(11111)
        logging.critical(11111)
        markets_carts = await BaseService().get_all(self.cart_model, user_id=user.id)
        if not markets_carts:
            return {
                'status': 'error',
                'description': 'cart is empty',
            }
        buy_request = await BaseService().create(
            BuyRequest,
            user_id=user.id,
            name=f'Покупа майнеров {user.email}',
        )
        value_usd = 0
        discount = 0
        for market_cart in markets_carts:
            await BaseService().create(
                BuyRequestMinerItem,
                buy_request=buy_request,
                miner_item=market_cart.miner_item,
                count=market_cart.count,
            )
            await BaseService().delete(self.cart_model, id_=market_cart.id)
            miner_sum = market_cart.miner_item.price * market_cart.count
            if market_cart.count >= market_cart.miner_item.discount_count:
                discount_value = value_to_float(
                    value=market_cart.miner_item.discount_value,
                    decimal=settings.rate_decimal,
                )
                discount += miner_sum * (discount_value / 100)
            value_usd += miner_sum
        value_usd -= discount
        currency = BillingCurrencies.USD
        value_usd_float = value_to_float(value=value_usd, decimal=settings.usd_decimal)
        value = value_usd
        if payment_type == BillingPaymentTypes.RUS_CARD:
            currency = BillingCurrencies.RUB
            rub_rate = await get_bybit_rub()
            value = value_to_int(value=value_usd_float * rub_rate, decimal=settings.rub_decimal)
        if payment_type == BillingPaymentTypes.BTC:
            currency = BillingCurrencies.BTC
            btc_price = await headframe_api.get_btc_price()
            value = value_to_int(value=value_usd_float / btc_price, decimal=settings.btc_decimal)
        billing = await BaseService().create(
            Billing,
            user_id=user.id,
            type=BillingTypes.BUY_REQUEST,
            currency=currency,
            payment_type=payment_type,
            state=BillingStates.WAITING,
            value=value,
            value_usd=value_usd,
        )
        await BaseService().create(BillingBuyRequest, billing_id=billing.id, buy_request_id=buy_request.id)
        return {
            'status': 'ok',
            'billing_id': billing.id,
            'billing_id': billing.id,
            'billing_id': billing.id,
        }
