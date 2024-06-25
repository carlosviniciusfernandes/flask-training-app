from datetime import datetime
from typing import Dict, Optional

from beanie import Document
from pydantic import BaseModel, Field


class Review(BaseModel):
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(Document):
    first_name: str
    last_name: str
    reviews: Optional[Dict[str, Review]] = None
