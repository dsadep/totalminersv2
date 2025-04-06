from flask import Blueprint, render_template, session, url_for, redirect, request

from admin.db.database import basic_get_all_asc, basic_update, basic_get, basic_get_all_desc
from admin.db.models import BuyRequest, BuyRequestStates, BuyRequestMinerItem, BillingBuyRequest
from admin.service import generate_buy_request_dict, generate_buy_request_miner_item_dict, \
    generate_billing_dict
from admin.utils import auth_required

buy_requests_router = Blueprint(name='buy_requests_router', import_name='buy_requests_router')


@buy_requests_router.get('/buy/requests')
@auth_required
def index():
    return render_template(
        'buy_requests.html',
        username=session['username'],
        buy_requests=[
            generate_buy_request_dict(buy_request=buy_request)
            for buy_request in basic_get_all_desc(BuyRequest)
        ],
    )


@buy_requests_router.get('/buy/requests/<id>')
@auth_required
def buy_request_page(id: int):
    buy_request = basic_get(BuyRequest, id=id)
    buy_request_billing = basic_get(BillingBuyRequest, buy_request_id=buy_request.id)
    buy_requests_miners_items = basic_get_all_asc(BuyRequestMinerItem, buy_request_id=buy_request.id)
    return render_template(
        'buy_request_page.html',
        username=session['username'],
        buy_request=generate_buy_request_dict(buy_request=buy_request),
        billing=generate_billing_dict(billing=buy_request_billing.billing),
        buy_requests_miners_items=[
            generate_buy_request_miner_item_dict(buy_request_miner_item=buy_request_miner_item)
            for buy_request_miner_item in buy_requests_miners_items
        ],
        states=BuyRequestStates().dict(),
    )


@buy_requests_router.post('/buy/requests/<id>')
@auth_required
def buy_request_page_post(id: int):
    buy_request = basic_get(BuyRequest, id=id)
    state = request.form['btn']
    states = [BuyRequestStates.WAIT, BuyRequestStates.IN_WORK, BuyRequestStates.COMPLETED, BuyRequestStates.CANCELLED]
    if state in states:
        basic_update(buy_request, state=state)
    return redirect(url_for('buy_requests_router.buy_request_page', id=id))
