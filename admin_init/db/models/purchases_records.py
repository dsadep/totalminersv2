import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from ..base_model import Model


class PurchaseRecord(Model):
    __tablename__ = 'purchases_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default="Покупка майнеров")
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    amount = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.datetime.now)
