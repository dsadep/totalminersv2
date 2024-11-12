from datetime import datetime

import pyotp
from fastapi import UploadFile, HTTPException, BackgroundTasks
from passlib.hash import pbkdf2_sha512

from api.db.models import User, ResetPasswordRequest, UserLangs
from api.schemas import UserRegister
from api.services.base import BaseService
from api.services.billings import BillingService
from api.services.images import ImageService
from api.utils import generate_otp, send_otp_email
from config import settings


class UserService:
    model = User

    async def get(self, user: User, id: int):
        user_db = await BaseService().get(self.model, id=id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User not found',
            )
        if user.id != user.id:
            raise HTTPException(
                status_code=401,
                detail="Cannot access to this user with your session",
            )
        return {
            'status': 'ok',
            'user': await UserService().generate_user_dict(user=user_db),
        }

    async def add_new_user(self, user_register: UserRegister) -> dict:
        if await BaseService().get(self.model, email=user_register.email):
            return {
                "result": False,
                "msg": 'User already exists',
                "status": 400,
            }
        await BaseService().create(
            self.model,
            email=user_register.email,
            lastname=user_register.lastname,
            firstname=user_register.firstname,
            phone=user_register.phone,
            password=pbkdf2_sha512.hash(user_register.password),
            last_totp='none',
            totp_sent=datetime(1970, 1, 1),
        )
        return {
            "result": True,
            "msg": None,
        }

    async def login_user(
            self,
            email: str,
            password: str,
            background_tasks: BackgroundTasks,
    ) -> dict:
        user = await BaseService().get(self.model, email=email)
        if not user:
            return {
                "status": 'error',
                "description": "user_not_found",
            }
        if not pbkdf2_sha512.verify(password, user.password):
            return {
                "status": 'error',
                "description": "wrong_password",
            }
        if not user.access_allowed:
            return {
                "status": 'error',
                'description': 'account_blocked',
            }
        code = generate_otp()
        await BaseService().update(user, last_totp=code, totp_sent=datetime.now())
        background_tasks.add_task(send_otp_email, email, code)
        return {
            "status": 'ok',
        }

    @staticmethod
    async def update_password(user: User, old_password: str, new_password: str, otp: str, ) -> dict:
        if not user.mfa_enabled:
            return {
                'status': 'error',
                'description': 'google 2fa required',
            }
        totp_auth = pyotp.TOTP(user.mfa_key)
        if otp != totp_auth.now():
            return {
                'status': 'error',
                'description': 'Wrong code',
            }
        if not pbkdf2_sha512.verify(old_password, user.password):
            return {
                'status': 'error',
                'description': 'wrong password',
            }
        await BaseService().update(user, password=pbkdf2_sha512.hash(new_password))
        return {
            'status': 'ok',
        }

    @staticmethod
    async def update_user_profile(
            user: User,
            firstname: str,
            lastname: str,
            phone: str,
            email: str,
            image_id: int,
            country: str,
            address: str,
            inn: str,
            profile_type: str,
            telegram: str,
    ) -> dict:
        await BaseService().update(
            user,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            email=email,
            telegram=telegram,
            iamge_id=image_id,
            country=country,
            address=address,
            inn=inn,
            profile_type=profile_type,
        )
        return {
            'status': 'ok',
        }

    @staticmethod
    async def generate_reset_password_request(user_id: int) -> ResetPasswordRequest:
        """
        Создает запрос на сброс пароля (забыл пароль) и привязывает к пользователю. Возвращает id запроса
        """
        request = await BaseService().create(ResetPasswordRequest, user_id=user_id, created_at=datetime.now())
        return request

    @staticmethod
    async def set_expired_reset_request(id: str):
        """
        Удаляет запрос, если пароль был сброшен
        """
        await BaseService().delete(ResetPasswordRequest, id_=id)

    @staticmethod
    async def update_wallet(user: User, wallet: str, otp: str) -> dict:
        if not user.mfa_enabled:
            return {
                'status': 'error',
                'description': 'google 2fa required',
            }
        totp_auth = pyotp.TOTP(user.mfa_key)
        if otp != totp_auth.now():
            return {
                'status': 'error',
                'description': 'Wrong code',
            }
        await BaseService().update(user, wallet=wallet)
        # await headframe_api.update_wallet(wallet_id=user.wallet_id, wallet=wallet)
        return {
            'status': 'ok',
        }

    @staticmethod
    async def delete_wallet(user: User, otp: str) -> dict:
        if not user.mfa_enabled:
            return {
                'status': 'error',
                'description': 'google 2fa required',
            }
        totp_auth = pyotp.TOTP(user.mfa_key)
        if otp != totp_auth.now():
            return {
                'status': 'error',
                'description': 'Wrong code',
            }
        await BaseService().update(user, wallet=None)
        # await headframe_api.update_wallet(wallet_id=user.wallet_id, wallet=None)
        return {
            'status': 'ok',
        }

    @staticmethod
    async def update_image(user: User, file: UploadFile) -> dict:
        image_id = (await ImageService().create(file=file))['image_id']
        await BaseService().update(user, image_id=image_id)
        return {
            'status': 'ok',
            'user': await UserService().generate_user_dict(user=user),
        }

    @staticmethod
    async def update_lang(user: User, lang: str) -> dict:
        lang_list = [UserLangs.RU, UserLangs.EN, UserLangs.HE]
        if lang not in lang_list:
            return {
                'status': 'error',
                'description': f'{lang} not in {lang_list}',
            }
        await BaseService().update(user, lang=lang)
        return {
            'status': 'ok',
            'user': await UserService().generate_user_dict(user=user),
        }

    @staticmethod
    async def generate_user_dict(user: User) -> dict:
        if not user:
            return {}
        return {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'phone': user.phone,
            'email': user.email,
            'password': user.password,
            'telegram': user.telegram,
            'image': await ImageService().generate_image_dict(image=user.image),
            'country': user.country,
            'address': user.address,
            'inn': user.inn,
            'profile_type': user.profile_type,
            'last_totp': user.last_totp,
            'totp_sent': user.totp_sent,
            'wallet': user.wallet,
            'mfa_key': user.mfa_key,
            'mfa_enabled': user.mfa_enabled,
            'miner_name': user.miner_name,
            'miner_id': user.miner_id,
            'wallet_id': user.wallet_id,
            'access_allowed': user.access_allowed,
            'lang': user.lang.upper(),
            'active_billings': await BillingService().active_billings(user=user),
            'created': user.created.strftime(format=settings.date_time_format),
        }
