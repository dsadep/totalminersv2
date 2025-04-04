import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, BigInteger
from sqlalchemy.orm import relationship

from ..base_model import Model


class PaymentTypes:
    REWARD = 'reward'
    HOSTING = 'hosting'
    PAYOUT = 'payout'


class PaymentCurrencies:
    USD = 'usd'
    BTC = 'btc'


class Payment(Model):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(length=32))
    currency = Column(String(length=8))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    value = Column(BigInteger, default=0)
    date = Column(String)
    date_time = Column(DateTime, default=datetime.datetime.now)
    created = Column(DateTime, default=datetime.datetime.now)
