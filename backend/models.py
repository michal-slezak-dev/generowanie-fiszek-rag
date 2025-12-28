from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel


class DeckStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"  # for decks that are generated but not saved yet

class User(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    username : str = Field(index=True)
    email : str = Field(index=True)

    decks : List['Deck'] = Relationship(back_populates='user')

class Deck(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    title : str
    description : Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: DeckStatus = Field(default=DeckStatus.DRAFT)

    user_id : Optional[int] = Field(default=None, foreign_key='user.id')
    user : Optional[User] = Relationship(back_populates='decks')
    
    flashcards : List['Flashcard'] = Relationship(back_populates='deck')

class Flashcard(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    front : str # question
    back : str # answer

    easiness_factor: float = Field(default=2.5)
    interval: int = Field(default=0)  # days
    repetitions: int = Field(default=0)
    next_review_date: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    deck_id : Optional[int] = Field(default_factory=None, foreign_key='deck.id')
    deck : Optional[Deck] = Relationship(back_populates='flashcards')

    review_logs: List["ReviewLog"] = Relationship(back_populates="flashcard")

class ReviewLog(SQLModel, table=True):
    """Tracks history of reviews for analytics"""
    id: Optional[int] = Field(default=None, primary_key=True)
    flashcard_id: int = Field(foreign_key="flashcard.id")
    
    review_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    grade: int  # user rating (0-5)
    
    # snapshot of our metrics AFTER this review
    resulting_interval: int
    resulting_easiness_factor: float
    
    flashcard: Optional[Flashcard] = Relationship(back_populates="review_logs")
