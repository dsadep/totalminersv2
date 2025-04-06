import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime

from ..base_model import Model


class MinerItemCategory(Model):
    __tablename__ = 'miner_items_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    is_hidden = Column(Boolean, default=False)
    priority = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.datetime.now)
