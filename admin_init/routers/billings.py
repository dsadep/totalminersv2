import logging
import time
from secrets import token_hex

from flask import Blueprint, render_template, session, request, url_for, redirect

from admin.db.database import basic_get_all_desc, basic_get, basic_update, basic_create
from admin.db.models import Billing, BillingStates, BillingTypes, BillingPaymentTypes, Image
from admin.service import generate_billing_dict
from admin.utils import auth_required
from config import settings

billings_router = Blueprint(name='billings_router', import_name='billings_router')


@billings_router.get('/billings')
@auth_required
def index():
    return render_template(
        'billings.html',
        username=session['username'],
        billings=[
            generate_billing_dict(billing=billing)
            for billing in basic_get_all_desc(Billing)
        ],
    )


@billings_router.get('/billing/<id>')
@auth_required
def page(id: int):
    billing = basic_get(Billing, id=id)
    return render_template(
        'billing_page.html',
        username=session['username'],
        billing=generate_billing_dict(billing=billing),
        types=BillingTypes().dict(),
        states=BillingStates().dict(),
        payment_types=BillingPaymentTypes().dict(),
    )


@billings_router.post('/billing/<id>/update/image')
def update_image(id: int):
    billing = basic_get(Billing, id=id)
    image_id = billing.image_id
    if request.files.get('image'):
        logging.critical(request.files['image'])
        file = request.files['image']
        extension = file.filename.split('.')[-1]
        path = f'{settings.image_dir}/{token_hex(8)}_{time.strftime("%Y%m%d%H%M")}.{extension}'
        file.save(path)
        image = basic_create(Image, path=path, filename=file.filename, extension=extension)
        image_id = image.id
        logging.critical(image_id)
    basic_update(billing, image_id=image_id)
    return redirect(url_for('billings_router.page', id=billing.id))


@billings_router.post('/billing/<id>/update/type')
@auth_required
def update_type(id: int):
    billing = basic_get(Billing, id=id)
    type_ = request.form['btn']
    if type_ in BillingTypes().list():
        basic_update(billing, type=type_)
    return redirect(url_for('billings_router.page', id=billing.id))


@billings_router.post('/billing/<id>/update/state')
@auth_required
def update_state(id: int):
    billing = basic_get(Billing, id=id)
    state = request.form['btn']
    if state in BillingStates().list():
        basic_update(billing, state=state)
    return redirect(url_for('billings_router.page', id=billing.id))
