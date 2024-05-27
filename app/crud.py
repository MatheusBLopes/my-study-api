from datetime import datetime

from sqlalchemy.future import select

from app.api.deps import SessionDep

from . import models, schemas


def get_card(db: SessionDep, card_id: int):
    stmt = select(models.Card).where(models.Card.id == card_id)
    result = db.exec(stmt).scalars().first()

    if result is None:
        return None

    sorted_reviews = sorted(
        result.reviews, key=lambda review: review.created_at, reverse=True
    )

    result.reviews = sorted_reviews

    return result


def get_cards(
    db: SessionDep,
    date: datetime = None,
    skip: int = 0,
    limit: int = 10,
):
    if date:
        stmt = (
            select(models.Card)
            .offset(skip)
            .limit(limit)
            .where(models.Card.next_review_date == date)
        )
    else:
        stmt = select(models.Card).offset(skip).limit(limit)

    cards = db.exec(stmt).scalars().all()

    for card in cards:
        sorted_reviews = sorted(
            card.reviews, key=lambda review: review.created_at, reverse=True
        )
        card.reviews = sorted_reviews

    return cards


def create_card(db: SessionDep, card: schemas.CardCreate, deck: schemas.DeckResponse):
    db_card = models.Card(side_a=card.side_a, side_b=card.side_b, deck=deck)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


# Function to update a card
def update_card(
    db: SessionDep, db_card: schemas.CardResponse, card_update: schemas.UpdateCard
):
    # Convert card_update to a dictionary and filter out None values
    update_data = card_update.model_dump(exclude_unset=True)

    # Update the card fields
    for key, value in update_data.items():
        setattr(db_card, key, value)

    # Commit the changes to the database
    db.commit()
    db.refresh(db_card)

    return db_card


def delete_card(db: SessionDep, card: models.Card):
    db.delete(card)
    db.commit()


def create_review(
    db: SessionDep, review: schemas.CardReviewResponse, quality: int, card: schemas.Card
):
    db_card_review = models.Review(
        quality=quality,
        easiness=review.easiness,
        interval=review.interval,
        repetitions=review.repetitions,
        review_date=review.review_date,
        card=card,
    )
    db.add(db_card_review)
    db.commit()
    db.refresh(db_card_review)
    return db_card_review


# DECKS
def get_deck(db: SessionDep, deck_id: int):
    stmt = select(models.Deck).where(models.Deck.id == deck_id)
    result = db.exec(stmt).scalars().first()

    if result is None:
        return None

    return result


def get_decks(
    db: SessionDep,
    skip: int = 0,
    limit: int = 10,
):
    stmt = select(models.Deck).offset(skip).limit(limit)
    decks = db.exec(stmt).scalars().all()

    return decks


def create_deck(db: SessionDep, deck: schemas.DeckCreate):
    db_deck = models.Deck(name=deck.name, description=deck.description)
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck


def delete_deck(db: SessionDep, deck: models.Deck):
    stmt = select(models.Card).where(models.Card.deck_id == deck.id)
    cards = db.exec(stmt).scalars().all()

    if cards:
        for card in cards:
            db.delete(card)

    db.delete(deck)
    db.commit()
