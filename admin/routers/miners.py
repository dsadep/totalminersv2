import logging
import time
from secrets import token_hex

from flask import session, render_template, request, redirect, url_for, Blueprint

from admin.db.database import basic_update, basic_create, basic_get_all_asc, basic_get, basic_delete
from admin.db.models import MinerItem, Image, MinerItemCategory
from admin.service import generate_miner_item_dict, generate_miner_item_category_dict
from admin.utils import auth_required, value_to_int
from config import settings

miners_router = Blueprint(name='miners_router', import_name='miners_router')


@miners_router.get('/miners')
@auth_required
def index():
    return render_template(
        'miners.html',
        username=session['username'],
        miners_items=[
            generate_miner_item_dict(miner_item=miner_item)
            for miner_item in basic_get_all_asc(MinerItem)
        ],
    )


@miners_router.get('/miners/<id>/')
@auth_required
def miner_page(id: int):
    miner_item = basic_get(MinerItem, id=id)
    return render_template(
        'miner_page.html',
        username=session['username'],
        miner_item=generate_miner_item_dict(miner_item=miner_item),
        categories=[
            generate_miner_item_category_dict(miner_item_category=miner_item_category)
            for miner_item_category in basic_get_all_asc(MinerItemCategory)
        ],
    )


@miners_router.post('/miners/<id>/')
@auth_required
def miner_page_post(id: int):
    miner_item = basic_get(MinerItem, id=id)
    price = float(request.form.get('price', 0))
    income = float(request.form.get('income', 0))
    hosting = float(request.form.get('hosting', 0))
    profit = float(request.form.get('profit', 0))
    discount_value = float(request.form.get('discount_value', 0))
    image_id = miner_item.image_id
    logging.critical(request.files.get('image'))
    if request.files.get('image'):
        logging.critical(request.files['image'])
        file = request.files['image']
        extension = file.filename.split('.')[-1]
        path = f'{settings.image_dir}/{token_hex(8)}_{time.strftime("%Y%m%d%H%M")}.{extension}'
        file.save(path)
        image = basic_create(Image, path=path, filename=file.filename, extension=extension)
        image_id = image.id
        logging.critical(image_id)
    basic_update(
        miner_item,
        name=request.form.get('name'),
        description=request.form.get('description'),
        category_id=int(request.form.get('category')),
        hash_rate=int(request.form.get('hash_rate')),
        energy_consumption=int(request.form.get('energy_consumption')),
        price=value_to_int(value=price, decimal=settings.usd_decimal),
        image_id=image_id,
        income=value_to_int(value=income, decimal=settings.usd_decimal),
        hosting=value_to_int(value=hosting, decimal=settings.usd_decimal),
        profit=value_to_int(value=profit, decimal=settings.usd_decimal),
        discount_count=int(request.form.get('discount_count', 0)),
        discount_value=value_to_int(value=discount_value, decimal=settings.rate_decimal),
        priority=int(request.form.get('priority')),
        is_hidden=request.form.get('ishidden') == 'on',
    )
    return redirect(url_for('miners_router.miner_page', id=id))


@miners_router.post('/miners/<id>/delete')
@auth_required
def miner_page_delete(id: int):
    basic_delete(MinerItem, id_=id)
    return redirect(url_for('miners_router.index'))


@miners_router.get('/miners/new')
@auth_required
def new_miner_page():
    return render_template(
        'miner_new.html',
        username=session['username'],
        categories=[
            generate_miner_item_category_dict(miner_item_category=miner_item_category)
            for miner_item_category in basic_get_all_asc(MinerItemCategory)
        ],
    )


@miners_router.post('/miners/new')
@auth_required
def new_miner_page_post():
    price = float(request.form.get('price', 0))
    income = float(request.form.get('income', 0))
    hosting = float(request.form.get('hosting', 0))
    profit = float(request.form.get('profit', 0))
    discount_value = float(request.form.get('discount_value', 0))
    file = request.files['image']
    extension = file.filename.split('.')[-1]
    path = f'{settings.image_dir}/{token_hex(8)}_{time.strftime("%Y%m%d%H%M")}.{extension}'
    file.save(path)
    image = basic_create(Image, path=path, filename=file.filename, extension=extension)
    miner_item = basic_create(
        MinerItem,
        name=request.form.get('name'),
        description=request.form.get('description'),
        category_id=int(request.form.get('category')),
        hash_rate=int(request.form.get('hash_rate')),
        energy_consumption=int(request.form.get('energy_consumption')),
        price=value_to_int(value=price, decimal=settings.usd_decimal),
        image_id=image.id,
        income=value_to_int(value=income, decimal=settings.usd_decimal),
        hosting=value_to_int(value=hosting, decimal=settings.usd_decimal),
        profit=value_to_int(value=profit, decimal=settings.usd_decimal),
        discount_count=int(request.form.get('discount_count')),
        discount_value=value_to_int(value=discount_value, decimal=settings.rate_decimal),
        priority=int(request.form.get('priority')),
        is_hidden=False,
    )
    return redirect(url_for('miners_router.miner_page', id=miner_item.id))
