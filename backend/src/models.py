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

    # TODO Read on Relations/Link for reviews
    # ref: https://dev.to/romanright/announcing-beanie-odm-18-relations-cache-actions-and-more-24ef
