from api.db.models import Feedback, FeedbackStates
from api.services.base import BaseService


class FeedbackService:
    model = Feedback

    async def create(self, name: str, phone: str) -> dict:
        feedback = await BaseService().get(self.model, phone=phone, state=FeedbackStates.WAIT)
        if feedback:
            return {
                'status': 'error',
                'description': f'Feedback with phone "{phone}" already exists'
            }
        feedback = await BaseService().create(self.model, name=name, phone=phone, state=FeedbackStates.WAIT)
        return {
            'status': 'ok',
            'feedback_id': feedback.id,
        }
