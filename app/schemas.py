from datetime import date
from pydantic import BaseModel


class Products(BaseModel):
    name: str
    quantity: int
    price: float
    category: str
    date: date

    class Config:
        from_attribute = True
