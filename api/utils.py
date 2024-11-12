import random
import smtplib
import string
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from retry import retry

from api.db.models import User
from api.services.base import BaseService
from api.services.settings import SettingsService
from config import settings


def generate_otp() -> str:
    """
    Создает одноразовый 4-значный код
    """
    letters = string.digits
    code = "".join([random.choice(letters) for i in range(4)])
    return code


@retry(delay=5, tries=10)
def send_otp_email(email, otp: str):
    """
    Отправляет одноразовый код по почте
    """
    msg = EmailMessage()
    msg["Subject"] = 'Код подтверждения в Total Miners'
    msg['From'] = settings.email_address
    msg['To'] = email
    msg.set_content(f"Ваш код подтверждения: {otp}")

    server = smtplib.SMTP(settings.email_server)
    server.starttls()
    server.login(settings.email_address, settings.email_password)
    server.send_message(msg)
    server.quit()
    print("Message sent")


@retry(delay=5, tries=10)
def send_reset_password_email(email: str, code: str):
    """
    Отправляет письмо с ссылкой на сброс пароля
    """
    msg = EmailMessage()
    msg["Subject"] = 'Сброс в Total Miners'
    msg['From'] = settings.email_address
    msg['To'] = email
    msg.set_content('\n'.join([
        f'Ссылка на сброс пароля: http://45.147.177.78/reset_password?token={code}',
        f'Действительна в течение суток',
    ]))

    server = smtplib.SMTP(settings.email_server)
    server.starttls()
    server.login(settings.email_address, settings.email_password)
    # server.sendmail(from_addr=config.EMAIL_ADDRESS,to_addrs=email,msg=f"Hello from TotalMiners, here is your one-time password: {otp}")
    server.send_message(msg)
    server.quit()
    print("Message sent")


def generate_token(email: str) -> str:
    """
    Генерирует токен авторизации на сайте
    """
    return jwt.encode(
        {
            'email': email,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=7)
        },
        settings.jwt_secret,
        algorithm="HS256",
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Возвращает объект пользователя для текущей сессии. Сессия определяется по токену
    """
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms='HS256')
        user = await BaseService().get(User, email=data['email'])
        if not user:
            raise HTTPException(
                status_code=403,
                detail='Detected jwt violation',
            )
        return user
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=403,
            detail='Invalid token',
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=403,
            detail='Token expired',
        )
    except:
        raise HTTPException(
            status_code=403,
            detail='Invalid token',
        )


def hash_to_tera_hash(value: float) -> float:
    if isinstance(value, str):
        value = float(value)
    return round(value / 10 ** 12, 2)


def hash_to_str(value: int) -> str:
    result = None
    if value / 10 ** 18 >= 1:
        result = round(value / 10 ** 18, 1)
        result = f'{result} EH/s'
    if value / 10 ** 15 >= 1:
        result = round(value / 10 ** 15, 1)
        result = f'{result} PH/s'
    elif value / 10 ** 12 >= 1:
        result = round(value / 10 ** 12, 1)
        result = f'{result} TH/s'
    elif value / 10 ** 9 >= 1:
        result = round(value / 10 ** 9, 1)
        result = f'{result} GH/s'
    elif value / 10 ** 6 >= 1:
        result = round(value / 10 ** 6, 1)
        result = f'{result} MH/s'
    elif value / 10 ** 3 >= 1:
        result = round(value / 10 ** 6, 1)
        result = f'{result} KH/s'
    else:
        result = f'{result} Hash/s'
    return result


def value_to_int(value: [str, float], decimal: int = settings.usd_decimal) -> int:
    if isinstance(value, str):
        value = float(value.replace(',', '.'))
    return int(value * 10 ** decimal)


def value_to_float(value: [str, int], decimal: int = settings.usd_decimal, round_value: int = None) -> float:
    if isinstance(value, str):
        value = int(value)
    result = value / 10 ** decimal
    if round_value:
        result = round(result, round_value)
    return result


async def get_hosting_by_hash_rate(
        hash_rate: float,
        electricity_consumption: float = None,
        electricity_cost: float = None,
) -> float:
    if not electricity_consumption:
        electricity_consumption = await SettingsService().get(key='hash_rate_electricity_consumption', default=15)
    if not electricity_cost:
        electricity_cost = await SettingsService().get(key='electricity_cost', default=0.06)
    return round(hash_rate * float(electricity_consumption) / 1_000 * float(electricity_cost) * 24, 2)
