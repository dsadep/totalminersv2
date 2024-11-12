from fastapi import APIRouter, Depends

from api.db.database import get_db
from api.services.country import CountryService

router = APIRouter(
    prefix='/countries',
)


@router.get(path='')
async def route():
    return await CountryService().get_all_countries()
