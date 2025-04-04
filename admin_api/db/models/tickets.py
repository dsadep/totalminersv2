import datetime

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..base_model import Model


class Ticket(Model):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
