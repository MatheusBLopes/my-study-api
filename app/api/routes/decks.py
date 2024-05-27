from fastapi import APIRouter, HTTPException, Query

from app import crud, schemas
from app.api.deps import SessionDep

router = APIRouter()


@router.post("/", response_model=schemas.DeckResponse)
def create_deck(deck: schemas.DeckCreate, db: SessionDep):
    return crud.create_deck(db=db, deck=deck)


@router.get("/{deck_id}", response_model=schemas.DeckResponse)
def read_deck(deck_id: int, db: SessionDep):
    db_deck = crud.get_deck(db, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck


@router.get("/", response_model=list[schemas.DeckResponse])
def read_decks(
    db: SessionDep,
    skip: int = Query(0, alias="skip"),
    limit: int = Query(10, alias="limit"),
):
    decks = crud.get_decks(db, skip=skip, limit=limit)
    return decks


@router.delete("/{deck_id}")
def delete_deck(deck_id: int, db: SessionDep):
    db_deck = crud.get_deck(db, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")

    crud.delete_deck(db, db_deck)
    return {"message": "Deck deleted"}
