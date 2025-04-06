import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, BigInteger
from sqlalchemy.orm import relationship

from ..base_model import Model


class BillingTypes:
    BUY_REQUEST = 'buy_request'
    HOSTING = 'hosting'

    def dict(self):
        return {
            'buy_request': self.BUY_REQUEST,
            'hosting': self.HOSTING,
        }

    def list(self):
        return [self.BUY_REQUEST, self.HOSTING]


class BillingStates:
    INVOICED = 'invoiced'
    WAITING = 'waiting'
    CONFIRMATION = 'confirmation'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    def dict(self):
        return {
            'invoiced': self.INVOICED,
            'waiting': self.WAITING,
            'confirmation': self.CONFIRMATION,
            'completed': self.COMPLETED,
            'canceled': self.CANCELED,
        }

    def list(self):
        return [self.INVOICED, self.WAITING, self.CONFIRMATION, self.COMPLETED, self.CANCELED]


class BillingPaymentTypes:
    RUS_CARD = 'rus_card'
    BTC = 'btc'
    USDT = 'usdt'

    def dict(self):
        return {
            'rus_card': self.RUS_CARD,
            'btc': self.BTC,
            'usdt': self.USDT,
        }

    def list(self):
        return [self.RUS_CARD, self.BTC, self.USDT]


class BillingCurrencies:
    USD = 'usd'
    BTC = 'btc'
    RUB = 'rub'


class Billing(Model):
    __tablename__ = 'billings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    image_id = Column(Integer, ForeignKey('images.id', ondelete='SET NULL'), nullable=True)
    image = relationship('Image', foreign_keys=image_id, uselist=False, lazy='selectin')
    type = Column(String(length=32))
    currency = Column(String(length=32))
    payment_type = Column(String(length=32))
    state = Column(String(length=32))
    value = Column(BigInteger, default=0)
    value_usd = Column(BigInteger, default=0)
    payment_data = Column(String(length=512))
    created = Column(DateTime, default=datetime.datetime.now)
