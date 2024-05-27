from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from supermemo2 import SMTwo

from app.api.crud import crud
from app.api.deps import SessionDep
from app.api.schemas import schemas

router = APIRouter()


@router.post("/", response_model=schemas.CardResponse)
def create_card(card: schemas.CardCreate, db: SessionDep):
    db_deck = crud.get_deck(db, deck_id=card.deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return crud.create_card(db=db, card=card, deck=db_deck)


@router.get("/{card_id}", response_model=schemas.CardResponse)
def read_card(card_id: int, db: SessionDep):
    db_card = crud.get_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card


@router.get("/", response_model=list[schemas.CardResponse])
def read_cards(
    db: SessionDep,
    date: datetime = None,
    skip: int = Query(0, alias="skip"),
    limit: int = Query(10, alias="limit"),
):
    cards = crud.get_cards(db, date, skip=skip, limit=limit)
    return cards


@router.put("/card-review/{card_id}", response_model=schemas.CardResponse)
def update_card_schedule(
    card_review: schemas.CardReviewCreate, card_id: int, db: SessionDep
):
    db_card = crud.get_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    if not db_card.reviews:
        review = SMTwo.first_review(card_review.quality)
    else:
        if datetime.now().strftime("%Y-%m-%d") == db_card.reviews[
            0
        ].created_at.strftime("%Y-%m-%d"):
            raise HTTPException(
                status_code=400, detail="You cant perform a new review today"
            )
        review = SMTwo(
            db_card.reviews[0].easiness,
            db_card.reviews[0].interval,
            db_card.reviews[0].repetitions,
        ).review(card_review.quality)

    crud.create_review(db, review, card_review.quality, db_card)
    crud.update_card(
        db, db_card, schemas.UpdateCard(next_review_date=review.review_date)
    )

    return db_card


@router.delete("/{card_id}")
def delete_card(card_id: int, db: SessionDep):
    deb_card = crud.get_card(db, card_id=card_id)
    if deb_card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    crud.delete_card(db, deb_card)
    return {"message": "Card deleted"}
