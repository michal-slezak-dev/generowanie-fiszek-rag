from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # security
from sqlmodel import Session, select
from database import create_db_and_tables, get_Session
from model import User, Deck, Flashcard
from contextlib import asynccontextmanager # db management in async mode
from typing import List, Dict

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home(): # multiapis at the same time async
    return {'status': 'OK'}

@app.post("/users/", response_model=User)
def create_user(user : User, session : Session = Depends(get_Session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/", response_model=List[User])
def read_users(session : Session = Depends(get_Session)):
    users = session.exec(select(User)).all()

    return users

@app.post("/deck/", response_model=Deck)
def create_deck(deck : Deck, session : Session = Depends(get_Session)):
    session.add(deck)
    session.commit()
    session.refresh(deck)
    return deck

@app.get("/decks/", response_model=List[Deck])
def read_decks(session : Session = Depends(get_Session)):
    decks = session.exec(select(Deck)).all()

    return decks

@app.post("/flashcard/", response_model=Flashcard)
def create_flashcard(flashcard : Flashcard, session : Session = Depends(get_Session)):
    session.add(flashcard)
    session.commit()
    session.refresh(flashcard)
    return flashcard

@app.get("/flashcards/", response_model=List[Flashcard])
def read_flashcards(session : Session = Depends(get_Session)): 
    flashcards = session.exec(select(Flashcard)).all()

    return flashcards

