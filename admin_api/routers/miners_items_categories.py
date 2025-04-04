from flask import jsonify, request, Blueprint

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
    """Получение категории товара майнинга по id."""
    miner_item_category = basic_get(MinerItemCategory, id=id)
    if not miner_item_category:
        return jsonify({"error": "Miner Item Category not found"}), 404
    return jsonify(generate_miner_item_category_dict(miner_item_category=miner_item_category)), 200




@miners_items_categories_router.get('/miners_items_categories/<id>')
@auth_required
def page(id: int):
    """Получение категории товара майнинга по id."""
    miner_item_category = basic_get(MinerItemCategory, id=id)
    if not miner_item_category:
        return jsonify({"error": "Miner Item Category not found"}), 404
    return jsonify(generate_miner_item_category_dict(miner_item_category=miner_item_category)), 200



@miners_items_categories_router.post('/miners_items_categories/<id>')
@auth_required
def page_post(id: int):
    """Обновление категории товара майнинга."""
    miner_item_category = basic_get(MinerItemCategory, id=id)
    if not miner_item_category:
        return jsonify({"error": "Miner Item Category not found"}), 404

    data = request.get_json()
    basic_update(
        miner_item_category,
        name=data.get('name'),
        description=data.get('description'),
        priority=int(data.get('priority')),
        is_hidden=data.get('is_hidden') == 'on',
    )
    return jsonify({"message": "Miner Item Category updated successfully"}), 200


@miners_items_categories_router.post('/miners_items_categories/<id>/delete')
@auth_required
def page_delete(id: int):
    """Удаление категории товара майнинга."""
    miner_item_category = basic_get(MinerItemCategory, id=id)
    if not miner_item_category:
        return jsonify({"error": "Miner Item Category not found"}), 404

    basic_delete(MinerItemCategory, id_=id)
    return jsonify({"message": "Miner Item Category deleted successfully"}), 200


@miners_items_categories_router.post('/miners_items_categories/create')
@auth_required
def create_post():
    """Создание новой категории товара майнинга."""
    data = request.get_json()
    
    miner_item_category = basic_create(
        MinerItemCategory,
        name=data.get('name'),
        description=data.get('description'),
        priority=int(data.get('priority')),
        is_hidden=data.get('is_hidden') == 'on',
    )
    
    return jsonify({"message": "Miner Item Category created successfully", "id": miner_item_category.id}), 201