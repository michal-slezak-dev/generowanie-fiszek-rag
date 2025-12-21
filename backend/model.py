from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    username : str = Field(index=True)
    email : str = Field(index=True)

    decks : List['Deck'] = Relationship(back_populates='user')

class Deck(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    title : str
    description : Optional[str] = None

    user_id : Optional[int] = Field(default=None, foreign_key='user.id')
    user : Optional[User] = Relationship(back_populates='decks')
    
    flashcards : List['Flashcard'] = Relationship(back_populates='deck')

class Flashcard(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    front : str # question
    back : str # answer

    deck_id : Optional[int] = Field(default_factory=None, foreign_key='deck.id')
    deck : Optional[Deck] = Relationship(back_populates='flashcards')


