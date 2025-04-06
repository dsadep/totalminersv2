from typing import Optional

from admin.db.models import User, Billing, BuyRequest, MinerItem, Image, Ticket, Message, MinerItemCategory, Feedback, \
    BuyRequestMinerItem, Worker
from admin.utils import hash_to_str, value_to_float
from config import settings


def generate_url(image: Image) -> Optional[str]:
    if not image:
        return
    return f'{settings.api_link}/api/images/get?id={image.id}'


def generate_image_dict(image: Image) -> Optional[dict]:
    if not image:
        return
    return {
        'id': image.id,
        'path': image.path,
        'url': generate_url(image=image),
        'filename': image.filename,
        'extension': image.extension,
        'created': image.created,
    }


def generate_user_dict(user: User) -> dict:
    if not user:
        return {}
    created = None
    if user.created:
        created = user.created.strftime(format=settings.date_time_format)
    return {
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'phone': user.phone,
        'email': user.email,
        'password': user.password,
        'telegram': user.telegram,
        'image': generate_image_dict(image=user.image),
        'country': user.country,
        'address': user.address,
        'inn': user.inn,
        'profile_type': user.profile_type,
        'last_totp': user.last_totp,
        'totp_sent': user.totp_sent,
        'wallet': user.wallet,
        'mfa_key': user.mfa_key,
        'mfa_enabled': user.mfa_enabled,
        'miner_name': user.miner_name,
        'miner_id': user.miner_id,
        'wallet_id': user.wallet_id,
        'access_allowed': user.access_allowed,
        'lang': user.lang.upper(),
        'created': created,
    }


def generate_billing_dict(billing: Billing) -> dict:
    if not billing:
        return {}
    return {
        'id': billing.id,
        'user': generate_user_dict(user=billing.user),
        'type': billing.type,
        'currency': billing.currency,
        'payment_type': billing.payment_type,
        'state': billing.state,
        'value': value_to_float(value=billing.value, decimal=settings.usd_decimal),
        'value_usd': value_to_float(value=billing.value, decimal=settings.usd_decimal),
        'image': generate_image_dict(image=billing.image),
        'created': billing.created.strftime(format=settings.date_time_format),
    }


def generate_buy_request_dict(buy_request: BuyRequest) -> dict:
    if not buy_request:
        return {}
    created = None
    if buy_request.created:
        created = buy_request.created.strftime(format=settings.date_time_format)
    return {
        'id': buy_request.id,
        'name': buy_request.name,
        'user': generate_user_dict(user=buy_request.user),
        'state': buy_request.state,
        'created': created,
    }


def generate_buy_request_miner_item_dict(buy_request_miner_item: BuyRequestMinerItem) -> dict:
    if not buy_request_miner_item:
        return {}
    return {
        'id': buy_request_miner_item.id,
        'buy_request': generate_buy_request_dict(buy_request=buy_request_miner_item.buy_request),
        'miner_item': generate_miner_item_dict(miner_item=buy_request_miner_item.miner_item),
        'count': buy_request_miner_item.count,
        'created': buy_request_miner_item.created.strftime(settings.date_time_format),
    }


def generate_miner_item_dict(miner_item: MinerItem) -> dict:
    if not miner_item:
        return {}
    return {
        'id': miner_item.id,
        'name': miner_item.name,
        'description': miner_item.description,
        'category': generate_miner_item_category_dict(miner_item_category=miner_item.category),
        'hash_rate': miner_item.hash_rate,
        'hash_rate_str': hash_to_str(value=miner_item.hash_rate),
        'energy_consumption': miner_item.energy_consumption,
        'price': value_to_float(value=miner_item.price, decimal=settings.usd_decimal),
        'image': generate_image_dict(image=miner_item.image),
        'discount_count': miner_item.discount_count,
        'discount_value': value_to_float(value=miner_item.discount_value, decimal=settings.rate_decimal),
        'priority': miner_item.priority,
        'is_hidden': miner_item.is_hidden,
    }


def generate_miner_item_category_dict(miner_item_category: MinerItemCategory) -> dict:
    if not miner_item_category:
        return {}
    return {
        'id': miner_item_category.id,
        'name': miner_item_category.name,
        'description': miner_item_category.description,
        'is_hidden': miner_item_category.is_hidden,
        'priority': miner_item_category.priority,
    }


def generate_ticket_dict(ticket: Ticket) -> dict:
    if not ticket:
        return {}
    return {
        'id': ticket.id,
        'title': ticket.title,
        'user': generate_user_dict(user=ticket.user),
        'is_open': ticket.is_open,
        'created': ticket.created_at.strftime(settings.date_time_format),
    }


def generate_feedback_dict(feedback: Feedback) -> dict:
    if not feedback:
        return {}
    return {
        'id': feedback.id,
        'name': feedback.name,
        'phone': feedback.phone,
        'state': feedback.state,
        'created': feedback.created.strftime(settings.date_time_format),
    }


def generate_message_dict(message: Message) -> dict:
    if not message:
        return {}
    return {
        'id': message.id,
        'ticket': generate_ticket_dict(ticket=message.ticket),
        'sender': message.sender,
        'content': message.content,
        'image': generate_image_dict(image=message.image) or None,
        'created': message.created_at.strftime(settings.date_time_format),
    }


def generate_miner_worker_dict(worker: Worker, workers_statuses: dict) -> dict:
    if not worker:
        return {}
    return {
        'id': worker.id,
        'id_str': worker.id_str,
        'name': worker.name,
        'behavior': worker.behavior,
        'user': generate_user_dict(user=worker.user),
        'miner_item': generate_miner_item_dict(miner_item=worker.miner_item),
        'status': workers_statuses.get(worker.id_str, 'unavailable'),
        'hidden': worker.hidden,
        'created': worker.created.strftime(format=settings.date_time_format),
    }
