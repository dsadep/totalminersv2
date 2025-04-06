from flask import Blueprint, request, jsonify
from datetime import datetime

from admin import basic_get
from admin.db.database import basic_get_all_asc, basic_create
from admin.db.models import Discount
from admin.db.database import basic_delete
from admin.utils import auth_required
from config import settings

discounts_router = Blueprint(name='discounts_router', import_name='discounts_router')

@discounts_router.get('/discounts')
@auth_required
def get_all_discounts():
    """Получение всех скидок."""
    discounts = [discount for discount in basic_get_all_asc(Discount)]
    return jsonify({"discounts": discounts})

@discounts_router.post('/discounts/<id>/delete')
@auth_required
def delete_discount(id: int):
    """Удаление скидки по ID."""
    discount = basic_get(Discount, id=id)
    if not discount:
        return jsonify({"error": "Скидка не найдена"}), 404

    basic_delete(Discount, id_=id)
    return jsonify({"message": "Скидка удалена"}), 200

@auth_required
def create_new_discount():
    """Создание новой скидки."""
    date_format = "%Y-%m-%dT%H:%M"

    # Получение данных из формы
    user_id = request.form.get('user_id')
    miner_id = request.form.get('miner_id')
    applies_to_electricity = 'applies_to_electricity' in request.form
    discount_percentage = float(request.form.get('discount_percentage', 0)) / 100
    is_active = 'is_active' in request.form
    expiration_date = request.form.get('expiration_date')
    expiration_date = datetime.strptime(expiration_date, date_format) if expiration_date else datetime.now()

    # Создание скидки
    discount = basic_create(
        Discount,
        user_id=user_id,
        miner_id=miner_id,
        applies_to_electricity=applies_to_electricity,
        discount_percentage=discount_percentage,
        is_active=is_active,
        expiration_date=expiration_date
    )

    return jsonify({"message": "Скидка успешно создана", "discount_id": discount.id}), 201
