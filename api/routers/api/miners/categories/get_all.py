from fastapi import APIRouter

from api.services.miners_categories import MinerCategoryService

router = APIRouter(
    prefix='/get/all',
)


@router.get('')
async def route():
    result = await MinerCategoryService().get_all()
    return result
