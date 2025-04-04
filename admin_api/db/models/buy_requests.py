import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from ..base_model import Model


class BuyRequestStates:
    WAIT = 'wait'
    IN_WORK = 'in_work'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    def dict(self):
        return {
            'wait': self.WAIT,
            'in_work': self.IN_WORK,
            'completed': self.COMPLETED,
            'cancelled': self.CANCELLED,
        }


class BuyRequest(Model):
    __tablename__ = 'buy_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    state = Column(String(length=32), default=BuyRequestStates.WAIT)
    created = Column(DateTime, default=datetime.datetime.now)
