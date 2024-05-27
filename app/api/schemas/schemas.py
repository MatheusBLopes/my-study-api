from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class QualityEnum(str, Enum):
    poor = "poor"
    average = "average"
    good = "good"


class CardReviewCreate(BaseModel):
    quality: int = Field(
        ..., ge=0, le=5, description="Quality of the card review, from 0 to 5"
    )
    easiness: Optional[float] = None
    interval: Optional[int] = None
    repetitions: Optional[int] = None
    review_date: Optional[datetime] = None


class CardReviewResponse(CardReviewCreate):
    created_at: datetime = Field(..., description="Creation date of the card review")


class CardBase(BaseModel):
    side_a: str = Field(..., description="Side A of the card")
    side_b: str = Field(..., description="Side B of the card")


class CardCreate(CardBase):
    deck_id: int = Field(..., description="Deck ID of the card")


class Card(CardBase):
    id: int = Field(..., description="ID of the card")


class CardResponse(CardBase):
    id: int = Field(..., description="ID of the card")
    created_at: datetime = Field(..., description="Creation date of the card")
    reviews: List[CardReviewResponse] = Field([], description="Reviews of the card")
    next_review_date: Optional[datetime] = Field(
        None, description="Next review date of the card"
    )
    deck_id: int = Field(..., description="Deck ID of the card")


class UpdateCard(BaseModel):
    side_a: Optional[str] = Field(None, description="Side A of the card")
    side_b: Optional[str] = Field(None, description="Side B of the card")
    next_review_date: Optional[datetime] = Field(
        None, description="Next review date of the card"
    )


class DeckBase(BaseModel):
    name: str = Field(..., description="Name of the deck")
    description: str = Field(..., description="Description of the deck")


class DeckCreate(DeckBase):
    pass


class DeckResponse(DeckBase):
    id: int = Field(..., description="ID of the deck")
    created_at: datetime = Field(..., description="Creation date of the deck")
    cards: List[CardResponse] = Field([], description="Cards in the deck")
