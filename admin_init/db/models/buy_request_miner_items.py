import datetime

from sqlalchemy import ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import relationship

from ..base_model import Model


class BuyRequestMinerItem(Model):
    __tablename__ = 'buy_request_miner_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    buy_request_id = Column(Integer, ForeignKey('buy_requests.id', ondelete='SET NULL'), nullable=True)
    buy_request = relationship('BuyRequest', foreign_keys=buy_request_id, uselist=False, lazy='selectin')
    miner_item_id = Column(Integer, ForeignKey('miner_items.id', ondelete='SET NULL'), nullable=True)
    miner_item = relationship('MinerItem', foreign_keys=miner_item_id, uselist=False, lazy='selectin')
    count = Column(Integer, default=1)
    created = Column(DateTime, default=datetime.datetime.now)
