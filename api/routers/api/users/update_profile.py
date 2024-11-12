from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.db.models import User
from api.services.user import UserService
from api.utils import get_current_user

router = APIRouter(
    prefix='/updateProfile',
)


class UserUpdateProfileSchema(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str
    image_id: int
    country: str
    address: str
    inn: str
    profiletype: str
    telegram: str


@router.post(path='')
async def route(schema: UserUpdateProfileSchema, user: User = Depends(get_current_user)):
    result = await UserService().update_user_profile(
        user=user,
        firstname=schema.firstname,
        lastname=schema.lastname,
        phone=schema.phone,
        email=schema.email,
        image_id=schema.image_id,
        telegram=schema.telegram,
        country=schema.country,
        address=schema.address,
        inn=schema.inn,
        profile_type=schema.profiletype,
    )
    return result
