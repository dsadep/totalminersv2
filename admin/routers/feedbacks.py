from flask import Blueprint, render_template, session, url_for, redirect, request

from admin import basic_get
from admin.db.database import basic_get_all_asc, basic_update
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
