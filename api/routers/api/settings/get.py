from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.services.settings import SettingsService

router = APIRouter(
    prefix='/get',
)


class SettingGetSchema(BaseModel):
    key: str


@router.get(path='')
async def route(schema: SettingGetSchema = Depends()):
    result = await SettingsService().get_router(key=schema.key)
    return result
