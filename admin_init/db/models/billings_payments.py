import datetime

from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship

from ..base_model import Model


class BillingPayment(Model):
    __tablename__ = 'billings_payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    billing_id = Column(Integer, ForeignKey('billings.id', ondelete='SET NULL'), unique=True)
    billing = relationship('Billing', foreign_keys=billing_id, uselist=False, lazy='selectin')
    payment_id = Column(Integer, ForeignKey('payments.id', ondelete='SET NULL'))
    payment = relationship('Payment', foreign_keys=payment_id, uselist=False, lazy='selectin')
    created = Column(DateTime, default=datetime.datetime.now)
