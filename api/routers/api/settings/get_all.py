from fastapi import APIRouter

from api.services.settings import SettingsService

router = APIRouter(
    prefix='/get/all',
)


@router.get(path='')
async def route():
    result = await SettingsService().get_all_router()
    return result
