from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CardReviewCreate(BaseModel):
    quality: int
    easiness: Optional[float] = None
    interval: Optional[int] = None
    repetitions: Optional[int] = None
    review_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class CardReviewResponse(BaseModel):
    quality: int
    easiness: Optional[float] = None
    interval: Optional[int] = None
    repetitions: Optional[int] = None
    review_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CardBase(BaseModel):
    side_a: str
    side_b: str


class CardCreate(CardBase):
    deck_id: int


class Card(CardBase):
    id: int

    class Config:
        from_attributes = True

class CardResponse(CardBase):
    id: int
    created_at: datetime
    reviews: List[CardReviewResponse] = []
    next_review_date: Optional[datetime] = None
    deck_id: int

    class Config:
        from_attributes = True

class UpdateCard(BaseModel):
    side_a: Optional[str] = None
    side_b: Optional[str] = None
    next_review_date: Optional[datetime] = None




class DeckBase(BaseModel):
    name: str
    description: str


class DeckCreate(DeckBase):
    pass


class DeckResponse(DeckBase):
    id: int
    created_at: datetime
    cards: List[CardResponse] = []

    class Config:
        from_attributes = True
