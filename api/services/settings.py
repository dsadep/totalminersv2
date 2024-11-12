from typing import Optional

from api.db.models import Setting
from api.services.base import BaseService


class SettingsService:
    model = Setting

    async def get_router(self, key: str) -> dict:
        return {
            'status': 'ok',
            'value': await self.get(key=key),
        }

    async def get_all_router(self) -> dict:
        return {
            'status': 'ok',
            'settings': [
                {
                    'key': setting.key,
                    'value': setting.value,
                }
                for setting in await BaseService().get_all(self.model)
            ],
        }

    async def get(self, key: str, default=None) -> Optional[str]:
        setting = await BaseService().get(self.model, key=key)
        if not setting:
            setting = await BaseService().create(self.model, key=key, value=default)
        return setting.value
