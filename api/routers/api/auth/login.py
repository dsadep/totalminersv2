from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr

from api.services.user import UserService

router = APIRouter(
    prefix='/login',
)


class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: str


@router.post('')
async def route(schema: AuthLoginSchema, background_tasks: BackgroundTasks):
    result = await UserService().login_user(
        email=schema.email,
        password=schema.password,
        background_tasks=background_tasks,
    )
    return result
