from flask import Blueprint, request, jsonify

from admin.db.database import basic_get_all_asc, basic_update, basic_get, get_top_users_by_hashrate
from admin.db.models import User
from admin.service import generate_user_dict
from admin.utils import auth_required, get_btc_usd_rate

users_router = Blueprint(name='users_router', import_name='users_router')


@users_router.get('/users')
@auth_required
def index():
    """Получение списка пользователей"""
    users = [generate_user_dict(user) for user in basic_get_all_asc(User)]
    return jsonify(users)


@users_router.get('/users/<id>')
@auth_required
def users_page(id: int):
    """Получение данных конкретного пользователя"""
    user = basic_get(User, id=id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    return jsonify(generate_user_dict(user))



@users_router.get('/users/<id>/block')
@auth_required
def users_block(id: int):
    """Блокировка пользователя"""
    user = basic_get(User, id=id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    basic_update(user, access_allowed=False)
    return jsonify({"message": "Пользователь заблокирован"})

@users_router.get('/users/<id>/unblock')
@auth_required
def users_unblock(id: int):
    """Разблокировка пользователя"""
    user = basic_get(User, id=id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404
    basic_update(user, access_allowed=True)
    return jsonify({"message": "Пользователь разблокирован"})


@users_router.post('/users/<id>/update')
@auth_required
def update_user(id):
    """Обновление информации о пользователе"""
    user = basic_get(User, id=id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    data = request.get_json()
    basic_update(
        user,
        firstname=data.get("firstname"),
        lastname=data.get("lastname"),
        phone=data.get("phone"),
        telegram=data.get("telegram"),
    )
    return jsonify({"message": "Пользователь обновлен", "user": generate_user_dict(user)})


@users_router.get('/users/get/top20')
def top20_users():
    btc_usd_rate = get_btc_usd_rate()
    top20 = get_top_users_by_hashrate(btc_usd_rate=btc_usd_rate)
    return jsonify(top20), 200