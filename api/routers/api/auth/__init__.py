from fastapi import APIRouter

from .disable_mfa import router as router_disable_mfa
from .enable_mfa import router as router_enable_mfa
from .get_mfa_url import router as router_get_mfa_url
from .login import router as router_login
from .register import router as router_register
from .validate_user_authorization import router as router_validate_user_authorization
from .veirfy_totp import router as router_veirfy_totp

router = APIRouter(
    prefix="/auth",
    tags=['Auth'],
)
routers = [
    router_login, router_register, router_veirfy_totp, router_validate_user_authorization, router_get_mfa_url,
    router_enable_mfa, router_disable_mfa,
]

[router.include_router(router_) for router_ in routers]
