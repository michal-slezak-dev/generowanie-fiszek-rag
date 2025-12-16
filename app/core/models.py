from pydantic import BaseModel, Field

class Flashcard(BaseModel):
    """Model dla pojedynczej fiszki"""
    question: str = Field(description="Ziezle pytanie na podstawie strony w wikipedii.")
    answer: str = Field(description="Zwięzła odpowiedź na pytanie.")

class FlashcardList(BaseModel):
    """Model zawierajacy liste wszystkich wygenerowanych fiszek."""
    flashcards: list[Flashcard] = Field(description="Lista wygenerowanych fiszek.")