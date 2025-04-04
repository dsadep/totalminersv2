from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, request, url_for, redirect, jsonify

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
    return render_template(
        'tickets.html',
        username=session['username'],
        tickets=[
            generate_ticket_dict(ticket=ticket)
            for ticket in basic_get_all_asc(Ticket)
        ],
    )


@tickets_router.get('/tickets/<id>')
@auth_required
def ticket_page(id: int):
    ticket = basic_get(Ticket, id=id)
    if not ticket:
        redirect(url_for('tickets_router.index'))
    return render_template(
        'ticket_page.html',
        ticket=generate_ticket_dict(ticket=ticket),
        messages=[
            generate_message_dict(message=message)
            for message in basic_get_all_asc(Message, ticket_id=ticket.id)
        ],
    )


@tickets_router.post('/tickets/<id>')
@auth_required
def ticket_page_post(id: int):
    ticket = basic_get(Ticket, id=id)
    if not ticket:
        redirect(url_for('tickets_router.index'))
    # processing file if exists
    if request.files['file']:
        file = request.files['file']
        extension = file.filename.split('.')[-1]
        # Warning! using /app/assets dir for file storage 
        path = f'assets/{token_hex(8)}_{time.strftime("%Y%m%d%H%M")}.{extension}'
        file.save(path)
        image = basic_create(Image, path=path, filename=file.filename, extension=extension)
        basic_create(Message, ticket_id=ticket.id, sender=MessageSender.ADMIN, content=request.form.get('msg'), image_id=image.id)
    else:
        basic_create(Message, ticket_id=ticket.id, sender=MessageSender.ADMIN, content=request.form.get('msg'))
    return redirect(url_for('tickets_router.ticket_page', id=ticket.id))

@tickets_router.get('/tickets/status/<status>')
@auth_required 
def tickets_sorted_by_status(status: bool):
    return render_template(
        'tickets.html',
        username=session['username'],
        tickets=[
            generate_ticket_dict(ticket=ticket)
            for ticket in basic_get_all_asc(Ticket, is_open=status)
        ],
    )

@tickets_router.get('/tickets/sort/<date>')
@auth_required
def tickets_sorted_by_date(date: datetime):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format", 400
    start_of_day = date_obj
    end_of_day = date_obj + timedelta(days=1)
    return render_template(
        'tickets.html',
        username=session['username'],
        tickets=[
            generate_ticket_dict(ticket=ticket)
            for ticket in get_tickets_sorted_by_date(start_of_day, end_of_day)
        ],
    )
