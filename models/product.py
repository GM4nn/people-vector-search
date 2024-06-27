from typing import Optional
from beanie import Document
from pydantic import Field

class Product(Document):
    id: str = Field(default_factory=str, alias="_id")
    ean: Optional[str]
    name: str
    description: Optional[str] = None
    current_price: float
    promo_price: Optional[float] = None
    store: str
    
    ean_embedding: list[float] = []
    name_embedding: list[float] = []
    description_embedding: list[float] = []

    class Settings:
        name = "products"
    