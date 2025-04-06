from datetime import datetime
import logging
from statistics import mean

from flask import Blueprint, request, render_template, redirect, url_for, flash

from admin.db.database import basic_get, basic_create, basic_update, basic_get_all_asc
from admin.db.models import User, Worker, MinerItem
from admin.modules.headframe import headframe_api
from admin.service import generate_extended_worker_dict, generate_user_dict, generate_miner_worker_dict, generate_miner_item_dict
from admin.utils import auth_required, HashRateTypes, hash_to_str

workers_router = Blueprint('workers_router', 'workers_router')


@workers_router.get('/workers')
@auth_required
def index():
    workers_db = basic_get_all_asc(Worker)
    
    base_workers_data = [
        {
            'hash_rate': worker.miner_item.hash_rate if worker.miner_item is not None else 0
        }
        for worker in workers_db
    ]
    all_hashrates = [worker['hash_rate'] for worker in base_workers_data if worker['hash_rate'] > 0]
    average_hashrate = mean(all_hashrates) if all_hashrates else 0
    workers_data = [
        generate_extended_worker_dict(worker=worker, average_hashrate=average_hashrate)
        for worker in workers_db
    ]

    active_workers = [worker for worker in workers_data if worker['is_active']]
    faulty_workers = [worker for worker in workers_data if not worker['is_active']]

    return render_template(
        'workers.html',
        workers=workers_data,
        active_workers=active_workers,
        faulty_workers=faulty_workers,
        total_workers=len(workers_data),
        faulty_workers_count=len(faulty_workers),
        total_hashrate=hash_to_str(sum(all_hashrates)),
        average_hashrate=hash_to_str(average_hashrate)
    )

"""Дописать проверку на неактивность"""
@workers_router.post('/workers/<id>/restore')
@auth_required
def restore_worker(id: int):
    worker = basic_get(Worker, id=id)
    if not worker:
        return {'error': f'No worker with id {id}'}
    if worker.is_active == True:
        return {'error': 'worker is already active'}
    
    basic_update(worker, is_active=True, status_last_updated = datetime.now())
    return redirect(url_for('workers_router.index'))



@workers_router.get('/workers/<id>/')
@auth_required
def users_workers_page(id: int):
    user = basic_get(User, id=id)
    workers_db = basic_get_all_asc(Worker, user_id=user.id)
    workers_site = headframe_api.get_miner_workers(user.miner_id)
    workers_statuses = {}
    for worker_site in workers_site.get('data', []):
        workers_statuses[worker_site['id']] = worker_site['status']
    return render_template(
        'users_workers.html',
        user=generate_user_dict(user=user),
        workers=[
            generate_miner_worker_dict(worker=worker, workers_statuses=workers_statuses)
            for worker in workers_db
        ],
    )


@workers_router.get('/workers/<worker_id>')
@auth_required
def worker_page(worker_id: int):
    worker = basic_get(Worker, id=worker_id)
    workers_statuses = {}
    for worker_site in headframe_api.get_miner_workers(worker.user.miner_id).get('data', []):
        workers_statuses[worker_site['id']] = worker_site['status']
    return render_template(
        'worker_page.html',
        user=generate_user_dict(user=worker.user),
        worker=generate_miner_worker_dict(worker=worker, workers_statuses=workers_statuses),
        miners_items=[
            generate_miner_item_dict(miner_item=miner_item)
            for miner_item in basic_get_all_asc(MinerItem)
        ],
    )


@workers_router.get('/workers/<id>/create')  # BOUNDARY CREATE
@auth_required
def create_boundary(id: int):
    user = basic_get(User, id=id)
    return render_template(
        'worker_create_boundary.html',
        user=generate_user_dict(user=user),
        hash_types=HashRateTypes().get_all(),
    )


@workers_router.post('/workers/<id>/create')  # BOUNDARY CREATE
@auth_required
def create_boundary_post(id: int):
    user = basic_get(User, id=id)
    name = request.form.get('name')
    donor_miner_id = request.form.get('donor_miner_id')
    hash_rate = request.form.get('hash_rate')
    hash_type = request.form.get('hash_type')
    miner_item_id = request.form.get('miner_item_id')
    if '' in [name, donor_miner_id, miner_item_id, hash_rate, hash_type]:
        flash(f'Все поля должны быть заполнены')
        return redirect(url_for('workers_router.create_boundary', id=id))
    if basic_get(Worker, user_id=user.id, name=name):
        flash(f'У пользователя уже есть воркер с названием "{name}"!')
        return redirect(url_for('workers_router.init_real', id=id))
    try:
        hash_rate = int(hash_rate) * HashRateTypes().get(hash_type)
    except:
        flash('Поле "Хэшрейт" должно быть числом')
        return redirect(url_for('workers_router.create_boundary', id=id))
    if hash_rate < 4294967296:
        flash('Поле "Хэшрейт" минимальное значение 4.29 GH/s')
        return redirect(url_for('workers_router.create_boundary', id=id))
    miner_item = basic_get(MinerItem, id=int(miner_item_id))
    if not miner_item:
        flash('Поле "ID Товара (майнера)" товар не найден')
        return redirect(url_for('workers_router.create_boundary', id=id))
    boundary = headframe_api.create_boundary(
        name=name,
        recipient_miner_id=user.miner_id,
        donor_miner_id=donor_miner_id,
        hash_rate=str(hash_rate),
    )
    if boundary.get('error'):
        flash(f'Ошибка: {boundary}')
        return redirect(url_for('workers_router.create_boundary', id=id))
    basic_create(
        Worker,
        id_str=boundary['id'],
        name=boundary['name'],
        behavior=boundary['behavior'],
        user_id=user.id,
        miner_item_id=miner_item.id,
        hidden=False,
    )
    return redirect(url_for('workers_router.users_workers_page', id=id))


@workers_router.get('/workers/<id>/delete')
@auth_required
def delete_worker(id: int):
    worker = basic_get(Worker, id=request.args.get('worker_id'))
    boundary = headframe_api.delete_boundary(worker_id=worker.id_str)
    if boundary.get('error'):
        flash(f'Ошибка: {boundary}')
        return redirect(url_for('workers_router.users_workers_page', id=id))
    basic_update(worker, hidden=True)
    return redirect(url_for('workers_router.users_workers_page', id=id))


@workers_router.post('/workers/<worker_id>/update')
@auth_required
def update(worker_id: int):
    worker = basic_get(Worker, id=worker_id)
    if not worker:
        flash('Воркер не найден')
        return redirect(url_for('workers_router.worker_page', worker_id=worker.id))
    id_str = request.form.get('id_str')
    if not id_str:
        id_str = None
    name = request.form.get('name')
    if not name:
        name = None
    behavior = request.form.get('behavior')
    if not behavior:
        behavior = None
    miner_item_id = request.form.get('miner_item_id')
    if not miner_item_id:
        miner_item_id = None
    else:
        miner_item_id = int(miner_item_id)
    hidden = request.form.get('hidden') == 'on'
    logging.critical(request.form)
    logging.critical([id_str, name, behavior, miner_item_id, hidden])
    basic_update(
        worker,
        id_str=id_str,
        name=name,
        behavior=behavior,
        miner_item_id=miner_item_id,
        hidden=hidden,
    )
    return redirect(url_for('workers_router.worker_page', worker_id=worker.id))
