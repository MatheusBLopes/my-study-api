from models import Card

def create_card() -> Card:
    db_item = Card.model_validate(item_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item