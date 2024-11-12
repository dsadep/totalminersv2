from api.db.models import Country
from api.schemas import CountryAdd
from api.services.base import BaseService


class CountryService:
    model = Country

    async def get_all_countries(self):
        return await BaseService().get_all(self.model)

    async def add_country(self, new_country: CountryAdd) -> dict:
        if await BaseService().get(self.model, name=new_country.name):
            return {
                'result': False,
                'msg': 'Country already exists'
            }
        await BaseService().create(self.model, name=new_country.name, short_code=new_country.short_code)
        return {
            'result': True,
        }
