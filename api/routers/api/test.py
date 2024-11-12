from fastapi import APIRouter, Depends

from api.db.database import get_db
from api.db.models import User
from api.modules.headframe import headframe_api
from api.services.base import BaseService
from api.services.country import CountryService

router = APIRouter(
    prefix='/test',
)


@router.get(path='')
async def route():
    user = await BaseService().get(User, id=23)
    # a = await headframe_api.update_wallet(wallet_id=user.wallet_id, wallet='1KaXJMQ1MQRmtJMH2eqoXR9QHqWREYy9mK')
    a = await headframe_api.update_wallet(wallet_id=user.wallet_id, wallet='1KaXJMQ1MQRmtJMH2eqoXR9QHqWREYy9mK')
    print(a)
    return {}
