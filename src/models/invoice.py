from datetime import date
from pydantic import BaseModel
from .item import Item

class Invoice(BaseModel):
    order_id: int
    date: date
    customer_id: str
    products: list[Item]