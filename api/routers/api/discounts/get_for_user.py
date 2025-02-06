from fastapi import APIRouter, Depends, HTTPException

from api.db.models import User
from api.services.discounts import DiscountService
from api.utils import get_current_user

router = APIRouter(
    prefix='/get',
)

@router.get(path='')
async def route(user: User = Depends(get_current_user)):
    try:
        result = await DiscountService().get_all_for_user(user_id=user.id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get discounts for user: {e}"
        )
