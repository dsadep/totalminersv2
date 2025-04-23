from datetime import datetime, timedelta
from fastapi import HTTPException
from api.db.models.payments import Payment, PaymentCurrencies, PaymentTypes
from api.db.models.purchases_records import PurchaseRecord
from api.db.models.users import User
from api.db.models.workers import Worker
from api.services.base import BaseService
from api.utils import hash_to_str
import httpx

class StatsService(BaseService):
    async def get_btc_usd_rate(self):
        async with httpx.AsyncClient() as client:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data["bitcoin"]["usd"]

    async def get_stats(self, id: int, days=0):
        user = await self.get(User, id=id)
        if not user:
            raise HTTPException(404, 'User not found')

        delta = datetime.now() - user.created

        # Фильтр по дате
        date_filter = None
        if days > 0:
            date_filter = datetime.now() - timedelta(days=days)

        # Аппараты пользователя (не скрытые)
        workers = await self.get_all(Worker, user_id=id, hidden=False)
        num_workers = len(workers)

        hash_rate = 0
        energy_total = 0
        if workers:
            for w in workers:
                if w.miner_item:
                    hash_rate += w.miner_item.hash_rate
                    energy_total += w.miner_item.energy_consumption

        # Затраты на хостинг
        custom_where_hosting = (Payment.date_time >= date_filter) if date_filter else None
        payments_hosting = await self.get_list(Payment, custom_where=custom_where_hosting, user_id=id, type=PaymentTypes.HOSTING)
        hosting_cost = sum(p.value for p in payments_hosting if p.currency == PaymentCurrencies.USD) / 100

        # Доход в BTC
        custom_where_reward = (Payment.date_time >= date_filter) if date_filter else None
        payments_reward = await self.get_list(Payment, custom_where=custom_where_reward, user_id=id, type=PaymentTypes.REWARD)
        total_reward_btc = sum(p.value for p in payments_reward if p.currency == PaymentCurrencies.BTC) / 1e8

        # Покупки оборудования
        custom_where_purchase = (PurchaseRecord.date >= date_filter) if date_filter else None
        purchases = await self.get_list(PurchaseRecord, custom_where=custom_where_purchase, user_id=id)
        total_invested = sum(p.amount for p in purchases) / 100

        btc_usd_rate = await self.get_btc_usd_rate()
        reward_usd = total_reward_btc * btc_usd_rate

        net_profit_usd = reward_usd - hosting_cost

        payback_percent = round(((reward_usd) / (total_invested or 1)) * 100)
        if payback_percent > 100:
            payback_percent = 100

        return {
            "time_with_us": str(delta),
            "hash_rate": hash_to_str(hash_rate) if hash_rate else hash_to_str(0),
            "num_workers": num_workers,
            "total_invested_usd": round(total_invested, 2),
            "payback_percent": payback_percent,
            "energy_consumption_kw": energy_total,
            "hosting_cost_usd": round(hosting_cost, 2),
            "reward_btc": round(total_reward_btc, 8),
            "reward_usd": round(reward_usd, 2),
            "net_profit_usd": round(net_profit_usd, 2),
            "btc_usd_rate": btc_usd_rate
        }
