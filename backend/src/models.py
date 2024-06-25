from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel


class Review(BaseModel):
    description: str
    created_at: datetime


class User(Document):
    first_name: str
    last_name: str
    reviews: Optional[list[Review]] = []
