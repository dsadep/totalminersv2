from flask import Blueprint, jsonify, request

from admin.db.database import basic_get_all_asc, basic_update, basic_get, basic_get_all_desc
from admin.db.models import BuyRequest, BuyRequestStates, BuyRequestMinerItem, BillingBuyRequest
from admin.service import generate_buy_request_dict, generate_buy_request_miner_item_dict, \
    generate_billing_dict
from admin.utils import auth_required

buy_requests_router = Blueprint(name='buy_requests_router', import_name='buy_requests_router')


@buy_requests_router.get('/buy/requests')
@auth_required
def get_all_buy_requests():
    """Получение всех запросов на покупку"""
    buy_requests = [
        generate_buy_request_dict(buy_request=buy_request)
        for buy_request in basic_get_all_desc(BuyRequest)
    ]
    return jsonify(buy_requests), 200


@buy_requests_router.get('/buy/requests/<id>')
@auth_required
def buy_request_page(id: int):
    """Получение запроса на покупку по id"""
    buy_request = basic_get(BuyRequest, id=id)
    if not buy_request:
        return jsonify({"error": "Buy request not found"}), 404

    buy_request_billing = basic_get(BillingBuyRequest, buy_request_id=buy_request.id)
    buy_requests_miners_items = basic_get_all_asc(BuyRequestMinerItem, buy_request_id=buy_request.id)

    response = {
        "buy_request": generate_buy_request_dict(buy_request=buy_request),
        "billing": generate_billing_dict(billing=buy_request_billing.billing) if buy_request_billing else None,
        "buy_requests_miners_items": [
            generate_buy_request_miner_item_dict(buy_request_miner_item=buy_request_miner_item)
            for buy_request_miner_item in buy_requests_miners_items
        ],
        "states": BuyRequestStates().dict()
    }

    return jsonify(response), 200


@buy_requests_router.post('/buy/requests/<id>')
@auth_required
def buy_request_page_post(id: int):
    """Обновление состояния запроса на покупку"""
    buy_request = basic_get(BuyRequest, id=id)
    if not buy_request:
        return jsonify({"error": "Buy request not found"}), 404

    data = request.get_json()
    state = data.get('state')
    
    if state not in [BuyRequestStates.WAIT, BuyRequestStates.IN_WORK, BuyRequestStates.COMPLETED, BuyRequestStates.CANCELLED]:
        return jsonify({"error": "Invalid state"}), 400

    basic_update(buy_request, state=state)
    return jsonify({"message": "Buy request state updated", "new_state": state}), 200