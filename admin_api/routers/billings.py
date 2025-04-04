import logging
import time
from secrets import token_hex

from flask import Blueprint, request, jsonify

from admin.db.database import basic_get_all_desc, basic_get, basic_update, basic_create
from admin.db.models import Billing, BillingStates, BillingTypes, BillingPaymentTypes, Image
from admin.service import generate_billing_dict
from admin.utils import auth_required
from config import settings

billings_router = Blueprint(name='billings_router', import_name='billings_router')


@billings_router.get('/billings')
@auth_required
def get_all_billings():
    """Получение всех биллингов."""
    billings = [generate_billing_dict(billing=billing) for billing in basic_get_all_desc(Billing)]
    return jsonify({"billings": billings})


@billings_router.get('/billing/<id>')
@auth_required
def get_billing(id: int):
    """Получение информации о конкретном биллинге."""
    billing = basic_get(Billing, id=id)
    if not billing:
        return jsonify({"error": "Биллинг не найден"}), 404
    
    billing_data = generate_billing_dict(billing=billing)
    return jsonify({
        "billing": billing_data,
        "types": BillingTypes().dict(),
        "states": BillingStates().dict(),
        "payment_types": BillingPaymentTypes().dict()
    })


@billings_router.post('/billing/<int:id>/update/image')
@auth_required
def update_billing_image(id: int):
    """Обновление изображения для биллинга."""
    billing = basic_get(Billing, id=id)
    if not billing:
        return jsonify({"error": "Биллинг не найден"}), 404
    
    image_id = billing.image_id
    if request.files.get('image'):
        file = request.files['image']
        extension = file.filename.split('.')[-1]
        path = f'{settings.image_dir}/{token_hex(8)}_{time.strftime("%Y%m%d%H%M")}.{extension}'
        file.save(path)
        image = basic_create(Image, path=path, filename=file.filename, extension=extension)
        image_id = image.id
    
    basic_update(billing, image_id=image_id)
    return jsonify({"message": "Изображение обновлено", "billing_id": billing.id}), 200


@billings_router.post('/billing/<int:id>/update/type')
@auth_required
def update_billing_type(id: int):
    """Обновление типа биллинга."""
    billing = basic_get(Billing, id=id)
    if not billing:
        return jsonify({"error": "Биллинг не найден"}), 404
    
    type_ = request.form.get('btn')
    if type_ in BillingTypes().list():
        basic_update(billing, type=type_)
        return jsonify({"message": "Тип биллинга обновлен", "billing_id": billing.id}), 200
    
    return jsonify({"error": "Неверный тип биллинга"}), 400

@billings_router.post('/billing/<int:id>/update/state')
@auth_required
def update_billing_state(id: int):
    """Обновление состояния биллинга."""
    billing = basic_get(Billing, id=id)
    if not billing:
        return jsonify({"error": "Биллинг не найден"}), 404
    
    state = request.form.get('btn')
    if state in BillingStates().list():
        basic_update(billing, state=state)
        return jsonify({"message": "Состояние биллинга обновлено", "billing_id": billing.id}), 200
    
    return jsonify({"error": "Неверное состояние биллинга"}), 400
