from typing import List, Optional
from beanie import Document
from pydantic import Field

class Person(Document):
    id: str = Field(default_factory=str, alias="_id")
    first_name: str
    last_name: Optional[str] = None
    gender: str
    email: str
    phone: str
    birth_date: str
    job_title: str
    products: List[str] = []
    
    class Settings:
        name = "people"