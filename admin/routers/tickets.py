from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from admin import basic_get
from admin.db.database import basic_get_all_asc, basic_create, get_tickets_sorted_by_date
from admin.db.models import Ticket, Message, Image
from admin.db.models.messages import MessageSender
from admin.service import generate_ticket_dict, generate_message_dict
from admin.utils import auth_required

import os
import time
from secrets import token_hex

tickets_router = Blueprint(name='tickets_router', import_name='tickets_router')


@tickets_router.get('/tickets')
@auth_required
def index():
    tickets = basic_get_all_asc(Ticket)
    open_tickets = [generate_ticket_dict(ticket) for ticket in tickets if ticket.is_open]
    closed_tickets = [generate_ticket_dict(ticket) for ticket in tickets if not ticket.is_open]

    sorted_tickets = open_tickets + closed_tickets
    return jsonify(sorted_tickets)

@tickets_router.get('/tickets/<id>')
@auth_required
def ticket_page(id: int):
    """Получение тикета по ID"""
    ticket = basic_get(Ticket, id=id)
    if not ticket:
        return jsonify({"error": "Тикет не найден"}), 404

    messages = [
        generate_message_dict(message=message)
        for message in basic_get_all_asc(Message, ticket_id=ticket.id)
    ]
    
    return jsonify(
        {
            "ticket": generate_ticket_dict(ticket=ticket),
            "messages": messages,
        }
    )


@tickets_router.post('/tickets/<id>')
@auth_required
def post_ticket_message(id):
    """Добавление сообщения в тикет"""
    ticket = basic_get(Ticket, id=id)
    if not ticket:
        return jsonify({"error": "Тикет не найден"}), 404
    # processing file if exists
    file = request.files.get("file")
    content = request.form.get("msg")
    if file:
        extension = file.filename.split(".")[-1]
        # Warning! using /app/assets dir for file storag
        path = f"assets/{token_hex(8)}_{time.strftime('%Y%m%d%H%M')}.{extension}"
        file.save(path)
        image = basic_create(Image, path=path, filename=file.filename, extension=extension)
        basic_create(
            Message,
            ticket_id=ticket.id,
            sender=MessageSender.ADMIN,
            content=content,
            image_id=image.id,
        )
    else:
        basic_create(
            Message,
            ticket_id=ticket.id,
            sender=MessageSender.ADMIN,
            content=content,
        )
    return jsonify({"message": "Сообщение добавлено", "ticket_id": ticket.id})

@tickets_router.get('/tickets/status/<status>')
@auth_required
def get_tickets_by_status(status: bool):
    tickets = basic_get_all_asc(Ticket, is_open=status)
    return jsonify([generate_ticket_dict(ticket=ticket) for ticket in tickets])


@tickets_router.get('/tickets/sort/<date>')
@auth_required
def get_tickets_by_date(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    start_of_day = date_obj
    end_of_day = date_obj + timedelta(days=1)

    tickets = get_tickets_sorted_by_date(start_of_day, end_of_day)

    open_tickets = [generate_ticket_dict(ticket) for ticket in tickets if ticket.is_open]
    closed_tickets = [generate_ticket_dict(ticket) for ticket in tickets if not ticket.is_open]

    sorted_tickets = open_tickets + closed_tickets

    return jsonify(sorted_tickets)

