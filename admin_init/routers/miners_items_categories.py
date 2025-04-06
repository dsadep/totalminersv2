from flask import session, render_template, request, redirect, url_for, Blueprint

from admin.db.database import basic_update, basic_create, basic_get_all_asc, basic_get, basic_delete
from admin.db.models import MinerItemCategory
from admin.service import generate_miner_item_category_dict
from admin.utils import auth_required

miners_items_categories_router = Blueprint(
    name='miners_items_categories_router',
    import_name='miners_items_categories_router',
)


@miners_items_categories_router.get('/miners_items_categories')
@auth_required
def index():
    return render_template(
        'miners_items_categories.html',
        username=session['username'],
        miners_items_categories=[
            generate_miner_item_category_dict(miner_item_category=miner_item_category)
            for miner_item_category in basic_get_all_asc(MinerItemCategory)
        ],
    )


@miners_items_categories_router.get('/miners_items_categories/<id>')
@auth_required
def page(id: int):
    miner_item_category = basic_get(MinerItemCategory, id=id)
    return render_template(
        'miners_items_categories_page.html',
        username=session['username'],
        miner_item_category=generate_miner_item_category_dict(miner_item_category=miner_item_category),
    )


@miners_items_categories_router.post('/miners_items_categories/<id>')
@auth_required
def page_post(id: int):
    miner_item_category = basic_get(MinerItemCategory, id=id)
    basic_update(
        miner_item_category,
        name=request.form.get('name'),
        description=request.form.get('description'),
        priority=int(request.form.get('priority')),
        is_hidden=request.form.get('ishidden') == 'on',
    )
    return redirect(url_for('miners_items_categories_router.page', id=id))


@miners_items_categories_router.post('/miners_items_categories/<id>/delete')
@auth_required
def page_delete(id: int):
    basic_delete(MinerItemCategory, id_=id)
    return redirect(url_for('miners_items_categories_router.index'))


@miners_items_categories_router.get('/miners_items_categories/create')
@auth_required
def create():
    return render_template(
        'miners_items_categories_create.html',
        username=session['username'],
    )


@miners_items_categories_router.post('/miners_items_categories/create')
@auth_required
def create_post():
    miner_item_category = basic_create(
        MinerItemCategory,
        name=request.form.get('name'),
        description=request.form.get('description'),
        priority=int(request.form.get('priority')),
        is_hidden=request.form.get('ishidden') == 'on',
    )
    return redirect(url_for('miners_items_categories_router.page', id=miner_item_category.id))
