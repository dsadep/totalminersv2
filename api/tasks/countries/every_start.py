from api.services.country import CountryService
from api.schemas import CountryAdd 
from sqlalchemy.exc import IntegrityError
import json
import aiofiles

async def insert_countries_if_not_exists(file_path="countries.json"):
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        contents = await file.read()
        countries_data = json.loads(contents)
        for country in countries_data:
            await CountryService().add_country(CountryAdd(name=country['name'], short_code=country['short_code'])) 
