from flask import Blueprint, request, jsonify
from datetime import datetime
from admin import basic_get
from admin.db.database import basic_get_all_asc, basic_create
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
    """Получение всех тикетов"""
    tickets = [generate_ticket_dict(ticket=ticket) for ticket in basic_get_all_asc(Ticket)]
    return jsonify(tickets)

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

@tickets_router.get('/tickets/status')
@auth_required
def status_sorted_tickets(status: bool):
    """��������� ���� ������� � ������������ ��������"""
    tickets = [generate_ticket_dict(ticket=ticket) for ticket in basic_get_all_asc(Ticket, is_open=status)]
    return jsonify(tickets)

@tickets_router.get('/tickets/date')
@auth_required
def date_sorted_tickets(date: datetime):
    """��������� ���� ������� �� ������������ ����"""
    tickets = [generate_ticket_dict(ticket=ticket) for ticket in basic_get_all_asc(Ticket, created_at=date)]
    return jsonify(tickets)

@tickets_router.get('/chabanm')
def test_admin():
    return jsonify({'message': 'hi'})
