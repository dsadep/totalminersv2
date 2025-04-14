from admin.db.database import basic_get, get_non_payments, resume_mining_for_user_logic, stop_mining_for_user_logic
from admin.db.models.users import User
from admin.utils import auth_required
from flask import Blueprint, jsonify

non_payments_router = Blueprint(name = 'non_payments_router', import_name = 'non_payments_router')

@non_payments_router.get('/non_payments')
@auth_required
def non_payments():
    non_payments = get_non_payments()
    return jsonify(non_payments), 200

@non_payments_router.post('/stop_mining/<user_id>')
@auth_required
def stop_mining_for_user(user_id: int):
    user = basic_get(User, id=user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    count = stop_mining_for_user_logic(user_id)
    return jsonify({'message': f'Mining stopped for user {user.email}, count: {count}'})

@non_payments_router.post('/resume_mining/<user_id>')
@auth_required
def resume_mining_for_user(user_id: int):
    user = basic_get(User, id=user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    count = resume_mining_for_user_logic(user_id)
    return jsonify({'message': f'Mining resumed for user {user.email}, count: {count}'})

