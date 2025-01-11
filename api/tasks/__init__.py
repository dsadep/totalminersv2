import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.tasks.balances.save import task_balance_save
from api.tasks.billings.payment_check import task_billing_payment_check
from api.tasks.hostings.every_day import task_hosting_every_day
from api.tasks.hostings.every_month import task_hosting_every_month
from api.tasks.payments.every_day import task_payment_every_day
from api.tasks.workers.check import task_worker_check
from api.tasks.countries.every_start import insert_countries_if_not_exists 
from logger import config_logger

TASKS = []
"""BALANCE"""
TASKS.extend([
    task_balance_save,
])
"""BILLING"""
TASKS.extend([
    task_billing_payment_check,
])
"""WORKERS"""
TASKS.extend([
    task_worker_check,
])


async def start_app_tasks() -> None:
    config_logger()
    scheduler = AsyncIOScheduler()
    """
    COUNTRIES
    """
    scheduler.add_job(
        func=insert_countries_if_not_exists,
        trigger='date', 
        run_date=datetime.datetime.now(),
    )
    """
    HOSTING
    """
    scheduler.add_job(
        name='task_hosting_every_day',
        func=task_hosting_every_day,
        misfire_grace_time=30,
        trigger='cron',
        hour=1,
        minute=0,
        next_run_time=datetime.datetime.now(),
    )
    scheduler.add_job(
        name='task_hosting_every_month',
        func=task_hosting_every_month,
        misfire_grace_time=30,
        trigger='cron',
        hour=1,
        minute=0,
        next_run_time=datetime.datetime.now(),
    )
    """
    PAYMENT
    """
    scheduler.add_job(
        name='task_payment_every_day',
        func=task_payment_every_day,
        misfire_grace_time=30,
        trigger='cron',
        hour=1,
        minute=0,
        next_run_time=datetime.datetime.now(),
    )
    scheduler.start()
    while True:
        tasks_names = [task.get_name() for task in asyncio.all_tasks()]
        [asyncio.create_task(coro=task(), name=task.__name__) for task in TASKS if task.__name__ not in tasks_names]
        await asyncio.sleep(10 * 60)
