import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, BigInteger
from sqlalchemy.orm import relationship

from ..base_model import Model


class Balance(Model):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    value = Column(BigInteger, default=0)
    date = Column(String)
    created = Column(DateTime, default=datetime.datetime.now)
