import asyncio
import logging

from api.db.models import User, Worker
from api.modules.headframe import headframe_api
from api.services.base import BaseService


async def function() -> None:
    for user in await BaseService().get_all(User):
        logging.critical(f'[task_worker_check] user #{user.id}')
        workers = await headframe_api.get_miner_workers(miner_id=user.miner_id)
        workers_site_id_str = []
        for worker in workers.get('data', []):
            workers_site_id_str.append(worker['id'])
            worker_db = await BaseService().get(Worker, user_id=user.id, id_str=worker['id'])
            if not worker_db:
                await BaseService().create(
                    Worker,
                    id_str=worker['id'],
                    name=worker['name'],
                    behavior=worker['behavior'],
                    user_id=user.id,
                    hidden=True,
                )
                continue
            if not worker_db.miner_item:
                await BaseService().update(worker_db, hidden=True)
        if workers.get('data') is None:
            continue
        for worker_db in await BaseService().get_all(Worker, user_id=user.id):
            if worker_db.id_str in workers_site_id_str:
                continue
            await BaseService().update(worker_db, hidden=True)


async def task_worker_check():
    logging.critical(f'[task_worker_check] start')
    while True:
        try:
            await function()
        except Exception as e:
            logging.critical(f'Exception \n {e}')
        # Old timing: await asyncio.sleep(6 * 60 * 60)
        # New:
        await asyncio.sleep(15 * 60)
