import asyncio

from api.tasks import start_app_tasks

loop = asyncio.get_event_loop()
loop.run_until_complete(start_app_tasks())
