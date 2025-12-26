from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from pydantic import BaseModel

from database import get_Session
from models import Flashcard, ReviewLog, Deck, DeckStatus
from services.sm2 import SM2Algorithm

router = APIRouter(prefix="/study", tags=["study"])
sm2_service = SM2Algorithm()

class ReviewSubmission(BaseModel):
    flashcard_id: int
    grade: int # 0-5

@router.get("/due")
def get_due_cards(user_id: int, session: Session = Depends(get_Session)):
    """Get all cards that are due for review from all active decks."""
    now = datetime.now(timezone.utc)
    
    statement = (
        select(Flashcard)
        .join(Deck)
        .where(Deck.user_id == user_id)
        .where(Deck.status == DeckStatus.ACTIVE)
        .where(Flashcard.next_review_date <= now)
    )
    cards = session.exec(statement).all()
    return cards

@router.post("/review")
def review_card(submission: ReviewSubmission, session: Session = Depends(get_Session)):
    card = session.get(Flashcard, submission.flashcard_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # calculate new review interval (schedule)
    new_interval, new_reps, new_ef = sm2_service.calculate(
        grade=submission.grade,
        repetitions=card.repetitions,
        interval=card.interval,
        easiness_factor=card.easiness_factor
    )
    
    # update card
    card.repetitions = new_reps
    card.interval = new_interval
    card.easiness_factor = new_ef
    
    # calculate next review date
    # if interval is 0 (failed/new), verify when to display it
    # interval 1 = tomorrow.
    card.next_review_date = datetime.now(timezone.utc) + timedelta(days=new_interval)
    session.add(card)
    
    # create log
    log = ReviewLog(
        flashcard_id=card.id,
        grade=submission.grade,
        resulting_interval=new_interval,
        resulting_easiness_factor=new_ef,
        review_date=datetime.now(timezone.utc)
    )
    session.add(log)
    session.commit()
    
    return {"status": "success", "next_review": card.next_review_date}
