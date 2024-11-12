import aiohttp

from api.db.models import User, Worker, MinerItem
from api.modules.headframe import headframe_api
from api.schemas import WorkerResponse
from api.services.base import BaseService
from config import settings


class HeadframeService:
    def __init__(self):
        self.base_url = 'https://pool.headframe.io/api/backend/v0.1'
        self.cookies = {
            'ory_session_relaxedwescoffeywmz1r7og': settings.token,
        }

    async def create_miner_account(self, user: User) -> None:
        """
        Создает майнер (сабаккаунт) на headframe и присваивает его пользвателю
        """
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(url=self.base_url + '/workers/random-name') as response:
                miner = await response.json()
                miner_name = miner['name']
            async with session.post(url=self.base_url + '/miners', json={"account_name": miner_name}) as response:
                miners = await response.json()
        await BaseService().update(
            user,
            miner_id=miners['id'],
            miner_name=miner_name,
            wallet_id=miners['wallets'][0],
        )

    async def get_miner_worker_info(self, user: User) -> dict:
        """
        Получает и возвращает информацию о воркерах майнера с Headframe
        """
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(url=self.base_url + f'/miners/{user.miner_id}/workers') as response:
                d = await response.json()
                return d['data']

    @staticmethod
    async def get_all_user_workers(user_id: int) -> list[WorkerResponse]:
        user = await BaseService().get(User, id=user_id)
        workers = await BaseService().get_all(Worker, user_id=user.id)
        headframe_workers = await headframe_api.get_miner_workers(miner_id=user.miner_id)
        response = [
            WorkerResponse(
                id=worker.id,
                item_name=worker.item_name,
                hosting_cost=worker.miner_item.hosting,
                profit=worker.miner_item.profit,
                dohod=worker.miner_item.income,
                rashod=worker.miner_item.energy_consumption,
                status=[
                    headframe_worker['status']
                    for headframe_worker in headframe_workers if headframe_worker['id'] == worker.worker_id
                ][0],
            )
            for worker in workers
        ]
        return response

    async def change_wallet_address(self, user: User) -> None:
        """
        Меняет адрес кошелька на Headframe
        Для успешной смены поле `user.wallet_id` не должно быть пустым и у пользователя должен быть создан майнер
        """
        if user.wallet_id is None:
            return
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            data = {
                'address': user.wallet,
            }
            async with session.post(url=self.base_url + f'/wallets/{user.wallet_id}/addresses', json=data) as response:
                # d = await response.json()
                pass
