import datetime

from sqlalchemy import Column, String, Integer, DateTime

from ..base_model import Model


class Employee(Model):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created = Column(DateTime, default=datetime.datetime.now)
