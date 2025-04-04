import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, BigInteger
from sqlalchemy.orm import relationship

from ..base_model import Model


class PaymentSite(Model):
    __tablename__ = 'payments_sites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey('payments.id', ondelete='SET NULL'))
    payment = relationship('Payment', foreign_keys=payment_id, uselist=False, lazy='selectin')
    site_id = Column(String(length=128))
    hash_rate = Column(BigInteger, default=0)
    created = Column(DateTime, default=datetime.datetime.now)
