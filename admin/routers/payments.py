from admin.db.database import basic_get, basic_get_all_asc
from admin.db.models.payments import Payment
from admin.service import generate_payments_dict
from admin.utils import auth_required
from flask import Blueprint, jsonify

payments_router = Blueprint(name = 'payments_router', import_name = 'payments_router')

@payments_router.get('/payments')
@auth_required
def get_all_payments():
    payments = basic_get_all_asc(Payment)
    return jsonify(
        [generate_payments_dict(payment) 
        for payment in payments]
    ), 200

@payments_router.get('/payments/<payment_id>')
@auth_required
def get_payments(payment_id: int):
    payment = basic_get(Payment, id=payment_id)
    if not payment:
        return jsonify({'error': 'payment not found'}), 404
    return jsonify(generate_payments_dict(payment)), 200