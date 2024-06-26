from typing import List, Optional
from beanie import Document, Link
from pydantic import Field

from models.product import Product

class Person(Document):
    id: str = Field(default_factory=str, alias="_id")
    first_name: str
    last_name: Optional[str] = None
    gender: str
    email: str
    phone: str
    birth_date: str
    job_title: str
    products: List[Link[Product]] = []

    first_name_embedding: List[float] = []
    last_name_embedding: List[float] = []
    email_embedding: List[float] = []
    phone_embedding: List[float] = []
    birth_date_embedding: List[float] = []
    job_title_embedding: List[float] = []

    class Settings:
        name = "people"