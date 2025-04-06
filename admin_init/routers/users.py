from flask import Blueprint, render_template, session, redirect, url_for, request

from admin.db.database import basic_get_all_asc, basic_update, basic_get
from admin.db.models import User
from admin.service import generate_user_dict
from admin.utils import auth_required

users_router = Blueprint(name='users_router', import_name='users_router')


@users_router.get('/users')
@auth_required
def index():
    return render_template(
        'users.html',
        username=session['username'],
        users=[
            generate_user_dict(user=user)
            for user in basic_get_all_asc(User)
        ],
    )

# @users_router.get('users/get/top20')
# @auth_required
# def top20_users():
#     users_db = basic_get_all_asc(User)


@users_router.get('/users/<id>')
@auth_required
def users_page(id: int):
    user = basic_get(User, id=id)
    return render_template(
        'users_page.html',
        username=session['username'],
        user=generate_user_dict(user=user),
    )


@users_router.get('/users/<id>/block')
@auth_required
def users_block(id: int):
    user = basic_get(User, id=id)
    basic_update(user, access_allowed=False)
    return redirect(url_for('users_router.users_page', id=id))


@users_router.get('/users/<id>/unblock')
@auth_required
def users_unblock(id: int):
    user = basic_get(User, id=id)
    basic_update(user, access_allowed=True)
    return redirect(url_for('users_router.users_page', id=id))


@users_router.post('/users/<id>/update')
@auth_required
def users_update(id: int):
    user = basic_get(User, id=id)
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    telegram = request.form.get('telegram')
    basic_update(user, firstname=firstname, lastname=lastname, phone=phone, telegram=telegram)
    return redirect(url_for('users_router.users_page', id=id))

