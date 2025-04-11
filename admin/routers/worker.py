from datetime import timedelta
import logging

from flask import Blueprint, request, jsonify

from admin.db.database import basic_get, basic_create, basic_update, basic_get_all_asc
from admin.db.models import User, Worker, MinerItem
from admin.modules.headframe import headframe_api
from admin.service import generate_user_dict, generate_miner_worker_dict, generate_miner_item_dict, generate_workers_dict
from admin.utils import auth_required, HashRateTypes

workers_router = Blueprint('workers_router', 'workers_router')

@workers_router.get('/workers')
@auth_required
def get_all_workers_grouped():
    """Возвращает всех воркеров, сгруппированных по активности."""
    workers_db = basic_get_all_asc(Worker)
    
    all_workers = []
    faulty_workers = []

    for worker in workers_db:
        worker_data = generate_workers_dict(worker)
        all_workers.append(worker_data)
        if not worker.is_active:
            faulty_workers.append(worker_data)

    return jsonify({
        "all": all_workers,
        "faulty": faulty_workers
    }), 200

                
@workers_router.get("/workers/<int:id>/")
@auth_required
def get_user_workers(id):
    """Получение всех воркеров пользователя."""
    user = basic_get(User, id=id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    workers_db = basic_get_all_asc(Worker, user_id=user.id)
    workers_site = headframe_api.get_miner_workers(user.miner_id)
    
    workers_statuses = {w["id"]: w["status"] for w in workers_site.get("data", [])}

    return jsonify(
        {
            "user": generate_user_dict(user),
            "workers": [
                generate_miner_worker_dict(worker, workers_statuses)
                for worker in workers_db
            ],
        }
    )

@workers_router.post('/workers/<id>/restore')
@auth_required
def restore_worker(id):
    worker = basic_get(Worker, id=id)
    if not worker:
        return jsonify({"error": "Worker not found"}), 404

    if worker.is_active:
        return jsonify({"message": "Worker is already active"}), 400

    basic_update(worker, is_active=True)

    return jsonify({
        "message": f"Worker {worker.id_str} is now active",
        "worker": generate_workers_dict(worker)
    }), 200

@workers_router.get("/workers/<int:worker_id>")
@auth_required
def get_worker(worker_id):
    """Получение информации о конкретном воркере."""
    worker = basic_get(Worker, id=worker_id)
    if not worker:
        return jsonify({"error": "Воркер не найден"}), 404

    workers_statuses = {
        w["id"]: w["status"]
        for w in headframe_api.get_miner_workers(worker.user.miner_id).get("data", [])
    }

    return jsonify(
        {
            "user": generate_user_dict(worker.user),
            "worker": generate_miner_worker_dict(worker, workers_statuses),
            "miners_items": [
                generate_miner_item_dict(item) for item in basic_get_all_asc(MinerItem)
            ],
        }
    )

@workers_router.post("/workers/<int:id>/create")
@auth_required
def create_worker(id):
    """Создание нового воркера."""
    user = basic_get(User, id=id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    data = request.get_json()
    name = data.get("name")
    donor_miner_id = data.get("donor_miner_id")
    hash_rate = data.get("hash_rate")
    hash_type = data.get("hash_type")
    miner_item_id = data.get("miner_item_id")

    if not all([name, donor_miner_id, miner_item_id, hash_rate, hash_type]):
        return jsonify({"error": "Все поля должны быть заполнены"}), 400

    if basic_get(Worker, user_id=user.id, name=name):
        return jsonify({"error": f'У пользователя уже есть воркер с названием "{name}"'}), 400

    try:
        hash_rate = int(hash_rate) * HashRateTypes().get(hash_type)
    except ValueError:
        return jsonify({"error": 'Поле "Хэшрейт" должно быть числом'}), 400

    if hash_rate < 4294967296:
        return jsonify({"error": 'Поле "Хэшрейт" минимальное значение 4.29 GH/s'}), 400

    miner_item = basic_get(MinerItem, id=int(miner_item_id))
    if not miner_item:
        return jsonify({"error": 'Поле "ID Товара (майнера)" товар не найден'}), 404

    boundary = headframe_api.create_boundary(
        name=name,
        recipient_miner_id=user.miner_id,
        donor_miner_id=donor_miner_id,
        hash_rate=str(hash_rate),
    )

    if boundary.get("error"):
        return jsonify({"error": boundary}), 400

    worker = basic_create(
        Worker,
        id_str=boundary["id"],
        name=boundary["name"],
        behavior=boundary["behavior"],
        user_id=user.id,
        miner_item_id=miner_item.id,
        hidden=False,
    )

    return jsonify({"message": "Воркер создан", "worker": generate_miner_worker_dict(worker)}), 201

@workers_router.delete("/workers/<int:id>/")
@auth_required
def delete_worker(id):
    """Удаление воркера."""
    worker_id = request.args.get("worker_id")
    worker = basic_get(Worker, id=worker_id)
    if not worker:
        return jsonify({"error": "Воркер не найден"}), 404

    response = headframe_api.delete_boundary(worker_id=worker.id_str)
    if response.get("error"):
        return jsonify({"error": response}), 400

    basic_update(worker, hidden=True)
    return jsonify({"message": "Воркер удален"}), 200


@workers_router.put("/workers/<int:worker_id>/")
@auth_required
def update_worker(worker_id):
    """Обновление информации о воркере."""
    worker = basic_get(Worker, id=worker_id)
    if not worker:
        return jsonify({"error": "Воркер не найден"}), 404

    data = request.get_json()

    basic_update(
        worker,
        id_str=data.get("id_str"),
        name=data.get("name"),
        behavior=data.get("behavior"),
        miner_item_id=int(data["miner_item_id"]) if data.get("miner_item_id") else None,
        hidden=data.get("hidden", False),
    )

    return jsonify({"message": "Воркер обновлен", "worker": generate_miner_worker_dict(worker)}), 200

