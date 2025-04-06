import datetime

from sqlalchemy import Column, String, Integer, DateTime

from ..base_model import Model


class Image(Model):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(length=256))
    filename = Column(String(length=128))
    extension = Column(String(8))
    created = Column(DateTime, default=datetime.datetime.now)
