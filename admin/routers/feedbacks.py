from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, url_for, redirect, request

from admin import basic_get
from admin.db.database import basic_get_all_asc, basic_get_all_desc, basic_get_sorted_asc, basic_get_sorted_desc, basic_update
from admin.db.models import Feedback
from admin.service import generate_feedback_dict
from admin.utils import auth_required

feedbacks_router = Blueprint(name='feedbacks_router', import_name='feedbacks_router')


@feedbacks_router.get('/feedbacks')
@auth_required
def index():
    return render_template(
        'feedbacks.html',
        username=session['username'],
        feedbacks=[
            generate_feedback_dict(feedback=feedback)
            for feedback in basic_get_all_asc(Feedback)
        ],
    )


@feedbacks_router.get('/feedbacks/update/state')
@auth_required
def update_state():
    id = request.args.get('id')
    state = request.args.get('state')
    feedback = basic_get(Feedback, id=id)
    if feedback and feedback.state != state:
        basic_update(feedback, state=state)
    return redirect(url_for('feedbacks_router.index'))

@feedbacks_router.get('/feedbacks/status/<status>')
@auth_required
def status_sorted_feedbacks(status: bool):
    return render_template(
        'feedbacks.html',
        username=session['username'],
        feedbacks=[
            generate_feedback_dict(feedback=feedback)
            for feedback in basic_get_all_asc(Feedback, state=status)
        ],
    )

@feedbacks_router.get('/feedbacks/date/asc')
@auth_required
def feedbacks_sorted_by_date_asc():
    return render_template(
        'feedbacks.html',
        username=session['username'],
        feedbacks=[
            generate_feedback_dict(feedback=feedback)
            for feedback in basic_get_sorted_asc(Feedback, Feedback.created)
        ],
    )

@feedbacks_router.get('/feedbacks/date/desc')
@auth_required
def feedbacks_sorted_by_date_desc():
    return render_template(
        'feedbacks.html',
        username=session['username'],
        feedbacks=[
            generate_feedback_dict(feedback=feedback)
            for feedback in basic_get_sorted_desc(Feedback, Feedback.created)
        ],
    )