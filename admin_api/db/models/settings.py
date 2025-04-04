from sqlalchemy import Column, String, Integer

from ..base_model import Model


class Setting(Model):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    value = Column(String)
