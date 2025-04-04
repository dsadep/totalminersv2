import datetime

from sqlalchemy import Column, String, Integer, DateTime

from ..base_model import Model


class FeedbackStates:
    WAIT = 'wait'
    CLOSE = 'close'


class Feedback(Model):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    phone = Column(String(length=32))
    state = Column(String(length=16))
    created = Column(DateTime, default=datetime.datetime.now)
