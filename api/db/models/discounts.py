from sqlalchemy import ForeignKey, Column, Integer, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from ..base_model import Model

class Discount(Model):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) 
    miner_id = Column(Integer, ForeignKey("miner_items.id"), nullable=True) 
    applies_to_electricity = Column(Boolean, default=False) 
    discount_percentage = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    expiration_date = Column(DateTime, nullable=True) 

    user = relationship("User", back_populates="discounts", cascade='all')
