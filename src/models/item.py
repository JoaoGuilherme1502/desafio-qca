from pydantic import BaseModel

class Item(BaseModel): 
    product_id: int
    product: str
    quantity: int
    unit_price: float
