import os
from app.services.rag_service import RAGService
from app.core.models import Flashcard

DEFAULT_URL = "https://en.wikipedia.org/wiki/Battle_of_Verdun"


def run_mvp():
    try:
        service = RAGService()
    except Exception as e:
        print(f"Blad inicjalizacji uslugi RAGService: {e}")
        return

    # ingestowanie
    print("\n--- INGESTOWANIE DANYCH -----------------------")
    wiki_url = input(f"Podaj link do Wikipedii (domyslnie: {DEFAULT_URL}): ")
    if not wiki_url:
        wiki_url = DEFAULT_URL

    service.ingest_url(wiki_url)

    print("\n--- GENERACJA FISZEK ---------------------")
    quiz_query = input("Wygeneruj 5 fiszek zawierajacych najwazniejsze fakty i informacje z tego artykułu.")
    if not quiz_query:
        quiz_query = "Wygeneruj 5 fiszek zawierajacych najwazniejsze fakty i informacje z tego artykułu."
    # generuje 5 fiszek
    flashcards: list[Flashcard] = service.generate_quiz(quiz_query, num_questions=5)

    if flashcards:
        print("\n==================================================")
        print("WYGENEROWANY QUIZ:")
        print("==================================================")
        for i, card in enumerate(flashcards):
            print(f"--- Karta {i + 1} ---")
            print(f"Pytanie: {card.question}")
            print(f"Odpowiedz: {card.answer}\n")
    else:
        print("\n Nie udalo sie wygenerowac fiszek. Sprawdz logi bledow.")


if __name__ == '__main__':
    try:
        import requests

        requests.get("http://localhost:11434") # defaultowy port dla Ollama
        run_mvp() # PROBLEM: STRASZNIE DŁUGO SIĘ WEKTORYZUJE TO... AŻ 8 MINUT czasami!!!
    except requests.exceptions.ConnectionError:
        print("\nBLAD: Nie mozna polaczyc sie z Ollama.")