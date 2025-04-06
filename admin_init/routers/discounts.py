from flask import Blueprint, render_template, session, request, url_for, redirect
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
def index():
    return render_template(
        'discounts.html',
        discounts=[
            discount
            for discount in basic_get_all_asc(Discount)
        ],
    )

@discounts_router.post('/discounts/<id>/delete')
@auth_required
def delete_discount(id: int):
    basic_delete(Discount, id_=id)
    return redirect(url_for('discounts_router.index'))

@discounts_router.get('/discounts/new')
@auth_required
def new_discount_form():
    return render_template('discounts_new.html')

@discounts_router.post('/discounts/new')
@auth_required
def new_discount():
    date_format = "%Y-%m-%dT%H:%M"

    # TODO!: add checking ids in db 
    user_id = request.form['user_id']
    miner_id = request.form['miner_id']
    applies_to_electricity = 'applies_to_electricity' in request.form
    discount_percentage = float(request.form['discount_percentage'])/100
    is_active = 'is_active' in request.form
    expiration_date = datetime.strptime(request.form['expiration_date'], date_format) or datetime.now() 

    basic_create(
        Discount,
        user_id=user_id,
        miner_id=miner_id,
        applies_to_electricity=applies_to_electricity,
        discount_percentage=discount_percentage,
        is_active=is_active,
        expiration_date=expiration_date
    )
    return redirect(url_for('discounts_router.index'))
