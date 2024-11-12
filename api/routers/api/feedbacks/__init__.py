from fastapi import APIRouter

from .create import router as router_create

router = APIRouter(
    prefix="/feedbacks",
    tags=['Feedbacks'],
)
routers = [
    router_create,
]
[router.include_router(router_) for router_ in routers]
