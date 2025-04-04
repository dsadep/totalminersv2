import datetime

from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship

from ..base_model import Model


class MarketCart(Model):
    __tablename__ = 'markets_carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    miner_item_id = Column(Integer, ForeignKey('miner_items.id', ondelete='SET NULL'), nullable=True)
    miner_item = relationship('MinerItem', foreign_keys=miner_item_id, uselist=False, lazy='selectin')
    count = Column(Integer, default=1)
    created = Column(DateTime, default=datetime.datetime.now)
