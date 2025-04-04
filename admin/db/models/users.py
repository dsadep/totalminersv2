import datetime

import pyotp
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..base_model import Model


class UserLangs:
    RU = 'ru'
    EN = 'en'
    HE = 'he'


class User(Model):
    """
    Модель пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    image_id = Column(Integer, ForeignKey('images.id', ondelete='SET NULL'), nullable=True)
    image = relationship('Image', foreign_keys=image_id, uselist=False, lazy='selectin')
    telegram = Column(String)
    country = Column(String)
    address = Column(String)
    inn = Column(String)
    profile_type = Column(String)
    last_totp = Column(String)
    totp_sent = Column(DateTime)
    wallet = Column(String)
    mfa_key = Column(String, default=pyotp.random_base32(), nullable=True)
    mfa_enabled = Column(Boolean, default=False, nullable=True)
    miner_name = Column(String)
    miner_id = Column(String)
    wallet_id = Column(String)
    access_allowed = Column(Boolean, default=True, nullable=True)
    lang = Column(String(length=4), default=UserLangs.RU)
    created = Column(DateTime, default=datetime.datetime.now)

    discounts = relationship("Discount", back_populates="user")
