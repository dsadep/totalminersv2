from api.db.models import MinerItemCategory
from api.services.base import BaseService
from config import settings


class MinerCategoryService:
    model = MinerItemCategory

    async def get(self, id_: int) -> dict:
        miner_item_category = await BaseService().get(self.model, id=id_, is_hidden=False)
        if not miner_item_category:
            return {
                'status': 'error',
                'description': f'Miner item category #{id_} not found',
            }
        return {
            'status': 'ok',
            'miner_item': await self.generate_miner_item_category_dict(miner_item_category=miner_item_category),
        }

    async def get_all(self) -> dict:
        miners_items_categories = await BaseService().get_all(self.model, is_hidden=False)
        return {
            'status': 'ok',
            'miners_items_categories': sorted(
                [
                    await self.generate_miner_item_category_dict(miner_item_category=miner_item_category)
                    for miner_item_category in miners_items_categories
                ],
                key=lambda x: x['priority'],
                reverse=True,
            ),
        }

    @staticmethod
    async def generate_miner_item_category_dict(miner_item_category: MinerItemCategory) -> dict:
        if not miner_item_category:
            return {}
        return {
            'id': miner_item_category.id,
            'name': miner_item_category.name,
            'description': miner_item_category.description,
            'is_hidden': miner_item_category.is_hidden,
            'priority': miner_item_category.priority,
            'created': miner_item_category.created.strftime(format=settings.date_time_format),
        }
