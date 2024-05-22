from supermemo2 import SMTwo
from fastapi import APIRouter, Query
from app.api.deps import (
    SessionDep,
)
from fastapi import HTTPException
from app import schemas, crud
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.DeckResponse)
def create_deck(deck: schemas.DeckCreate, db: SessionDep):
    return crud.create_deck(db=db, deck=deck)

@router.get("/{deck_id}", response_model=schemas.DeckResponse)
def read_card(deck_id: int, db: SessionDep):
    db_deck = crud.get_deck(db, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck

@router.get("/", response_model=list[schemas.DeckResponse])
def read_decks(db: SessionDep, skip: int = Query(0, alias="skip"), limit: int = Query(10, alias="limit"), ):
    decks = crud.get_decks(db, skip=skip, limit=limit)
    return decks
