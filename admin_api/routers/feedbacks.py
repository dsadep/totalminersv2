from flask import Blueprint, jsonify, request

from admin import basic_get
from admin.db.database import basic_get_all_asc, basic_update
from admin.db.models import Feedback
from admin.service import generate_feedback_dict
from admin.utils import auth_required

feedbacks_router = Blueprint(name='feedbacks_router', import_name='feedbacks_router')


@feedbacks_router.get('/feedbacks')
@auth_required
def get_all_feedbacks():
    """Получение списка всех отзывов."""
    feedbacks = basic_get_all_asc(Feedback)
    return jsonify({
        'feedbacks': [generate_feedback_dict(feedback=feedback) for feedback in feedbacks]
    }), 200


@feedbacks_router.get('/feedbacks/update/state')
@auth_required
def update_state():
    """Обновление состояния отзыва."""
    data = request.get_json()
    feedback_id = data.get('id')
    state = data.get('state')
    if not feedback_id or not state:
        return jsonify({"error": "ID отзыва и состояние обязательно для обновления"}), 400
    feedback = basic_get(Feedback, id=feedback_id)
    if not feedback:
        return jsonify({"error": "Отзыв не найден"}), 404
    if feedback.state != state:
        basic_update(feedback, state=state)

    return jsonify({"message": "Состояние отзыва успешно обновлено"}), 200