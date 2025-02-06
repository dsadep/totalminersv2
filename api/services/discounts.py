from datetime import datetime
from typing import Optional
from api.db.models import Discount
from api.services.base import BaseService

class DiscountService:
    model = Discount

    def generate_discount_dict(self, discount: Discount):
        return {
            "id": discount.id,
            "user_id": discount.user_id,  
            "miner_id": discount.miner_id, 
            "applies_to_electricity": discount.applies_to_electricity,
            "discount_percentage": discount.discount_percentage,
            "is_active": discount.is_active,
            "expiration_date": discount.expiration_date
        } 


    async def get_all_for_user(self, user_id: int) -> dict:
        user_discounts = await BaseService().get_all(self.model, user_id=user_id)
        return {
            "status": "ok",
            "discounts": [
                self.generate_discount_dict(discount)
                for discount in user_discounts 
            ]
        }


    async def create(
        self,
        miner_id: Optional[int] = None,
        user_id: Optional[int] = None,
        applies_to_electricity: Optional[bool] = None,
        discount_percentage: float = 0.0,
        is_active: bool = True, 
        expiration_date: Optional[datetime] = None
    ) -> Discount:
        await BaseService().create(
            self.model,
            miner_id=miner_id,
            user_id=user_id,
            applies_to_electricity=applies_to_electricity,
            discount_percentage=discount_percentage,
            is_active=is_active,
            expiration_date=expiration_date
        )
        return {
            "status": "ok"
        }
