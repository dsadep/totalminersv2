import datetime

from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship

from ..base_model import Model


class BillingBuyRequest(Model):
    __tablename__ = 'billings_buy_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    billing_id = Column(Integer, ForeignKey('billings.id', ondelete='SET NULL'), unique=True)
    billing = relationship('Billing', foreign_keys=billing_id, uselist=False, lazy='selectin')
    buy_request_id = Column(Integer, ForeignKey('buy_requests.id', ondelete='SET NULL'), nullable=True)
    buy_request = relationship('BuyRequest', foreign_keys=buy_request_id, uselist=False, lazy='selectin')
    created = Column(DateTime, default=datetime.datetime.now)
