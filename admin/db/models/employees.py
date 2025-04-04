import datetime
import enum

from sqlalchemy import Column, Enum, String, Integer, DateTime

from ..base_model import Model

class RoleEnum(enum.Enum):
    admin = 'admin'
    operator = 'operator'

class Employee(Model):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.operator)
    created = Column(DateTime, default=datetime.datetime.now)
