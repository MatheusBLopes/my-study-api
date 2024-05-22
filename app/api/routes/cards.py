from supermemo2 import SMTwo
from fastapi import APIRouter
from app.api.deps import (
    SessionDep,
)

router = APIRouter()

@router.get("/")
async def read_root(session: SessionDep):
    return {"Hello": "World"}
    # review = SMTwo.first_review(4)
    # review = SMTwo(review.easiness, review.interval, review.repetitions).review(5)
    # print(review)
    # review = SMTwo(review.easiness, review.interval, review.repetitions).review(5)

    # return review