from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData(schema="my_study_api"))


class Deck(Base):
    __tablename__ = "decks"
    __table_args__ = {"schema": "my_study_api"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String,
    )
    description = Column(
        String,
    )
    created_at = Column(DateTime, default=func.now(), nullable=False)

    cards = relationship("Card", back_populates="deck")


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = {"schema": "my_study_api"}
    id = Column(Integer, primary_key=True, index=True)
    side_a = Column(
        String,
    )
    side_b = Column(
        String,
    )
    next_review_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    deck = relationship("Deck", back_populates="cards")

    reviews = relationship("Review", back_populates="card")


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {"schema": "my_study_api"}
    id = Column(Integer, primary_key=True, index=True)
    easiness = Column(Float)
    interval = Column(Integer)
    repetitions = Column(Integer)
    review_date = Column(Date)
    quality = Column(Integer)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    card_id = Column(Integer, ForeignKey("cards.id"))
    card = relationship("Card", back_populates="reviews")
