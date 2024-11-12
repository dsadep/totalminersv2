from fastapi import APIRouter

from .get_countries import router as router_get_countries
from .get_user_by_id import router as router_get_user_by_id
from .require_reset_password import router as router_require_reset_password
from .reset_password import router as router_reset_password
from .set_wallet import router as router_set_wallet
from .update_image import router as router_update_image
from .update_lang import router as router_update_lang
from .update_password import router as router_update_password
from .update_profile import router as router_update_profile
from .delete_wallet import router as router_delete_wallet

router = APIRouter(
    prefix="/users",
    tags=['Users'],
)
routers = [
    router_get_countries, router_get_user_by_id, router_update_password, router_update_profile,
    router_require_reset_password, router_reset_password,router_update_image, router_update_lang,
    router_set_wallet, router_delete_wallet,
]

[router.include_router(router_) for router_ in routers]
