import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from ..base_model import Model

class WorkerBehaviors:
    HARDWARE = 'hardware'
    BOUNDARY = 'boundary'


class Worker(Model):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_str = Column(String(length=64))
    name = Column(String(length=128))
    behavior = Column(String(length=32))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), index=True)
    user = relationship('User', foreign_keys=user_id, uselist=False, lazy='selectin')
    miner_item_id = Column(Integer, ForeignKey('miner_items.id', ondelete='SET NULL'), nullable=True, index=True)
    miner_item = relationship('MinerItem', foreign_keys=miner_item_id, uselist=False, lazy='selectin')
    hidden = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=False)
    status_last_updated = Column(DateTime, default=func.now())