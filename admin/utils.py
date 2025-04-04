from functools import wraps

from flask import session, url_for, redirect, render_template

from config import settings


class HashRateTypes:
    HASH = 'Hash/s'
    KH = 'KH/s'
    MH = 'MH/s'
    GH = 'GH/s'
    TH = 'TH/s'
    PH = 'PH/s'

    def get_all(self) -> list:
        return [self.HASH, self.KH, self.MH, self.GH, self.TH, self.PH]

    def get(self, hash_type: str) -> int:
        return {
            self.HASH: 10 ** 0,
            self.KH: 10 ** 3,
            self.MH: 10 ** 6,
            self.GH: 10 ** 9,
            self.TH: 10 ** 12,
            self.PH: 10 ** 15,
        }.get(hash_type, 1)


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged' in session:
            return func(*args, **kwargs)
        return redirect(url_for('login_page'))

    return wrapper

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = session.get('role')   
            if user_role != role or user_role != 'admin':
                return render_template('access_forbidden.html')
            return func(*args, **kwargs)
        return wrapper  
    return decorator
  

def value_to_int(value: [str, float], decimal: int = settings.usd_decimal) -> int:
    if isinstance(value, str):
        value = float(value.replace(',', '.'))
    return int(value * 10 ** decimal)


def value_to_float(value: [str, int], decimal: int = settings.usd_decimal) -> float:
    if isinstance(value, str):
        value = int(value)
    return value / 10 ** decimal



def hash_to_str(value: int) -> str:
    result = 0
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
