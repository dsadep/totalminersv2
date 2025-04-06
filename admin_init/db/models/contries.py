from sqlalchemy import Column, String, Integer

from ..base_model import Model


class Country(Model):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    short_code = Column(String)
