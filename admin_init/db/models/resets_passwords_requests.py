import datetime
import uuid

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship

from ..base_model import Model


class ResetPasswordRequest(Model):
    """
    Модель запроса на сброс пароля
    """
    __tablename__ = 'resets_passwords_requests'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    expired = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
