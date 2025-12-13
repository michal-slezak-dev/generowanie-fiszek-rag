# WikiQuiz AI: Intelligent Flashcard & Quiz Generator
Przedmiot: Programowanie w Językach Funkcyjnych\
Autor: Michał Ślęzak WCY23IJ2S1 860 65\
Prowadzący laboratorium: mgr inż. Piotr Bączyk


## Opis Projektu

**WikiQuiz AI** to projekt zaliczeniowy z przedmiotu PJF - generator quizów i fiszek edukacyjnych, który wykorzystuje artykuły Wikipedii jako źródło wiedzy. Aplikacja automatycznie przetwarza dowolny artykuł, wyodrębnia kluczowe informacje i generuje fiszki/quizy do nauki z wykorzystaniem RAG (Retrieval-Augmented Generation).
## Planowane, kluczowe funkcjonalności (w zależności od czasu...)

| Kategoria | Funkcjonalność | Opis                                                                                                                                                      |
| :--- | :--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Generowanie** | RAG Pipeline | Wykorzystanie LangChain i ChromaDB do kontekstowego generowania pytań na podstawie wyszukanych fragmentów tekstu.                                         |
| **Baza Wiedzy** | Wektorowa Baza Danych | Indeksowanie tekstu z URL Wikipedii w **ChromaDB** w celu szybkiego wyszukiwania.                                                                         |
| **Trwałość Danych** | **Zapis Stanu (SQL)** | Użycie tradycyjnej relacyjnej bazy danych (np. SQLite/PostgreSQL) do **trwałego przechowywania wygenerowanych fiszek** oraz ich stanów nauki (dane SM-2). |
| **Uczenie** | Algorytm SM-2 (SRS) | Implementacja algorytmu SuperMemo-2 w Pythonie do wyznaczania optymalnych interwałów powtórek.                                              |

### Pipeline RAG (Retrieval-Augmented Generation)

1. **Ingestion:** Użytkownik podaje URL, który następnie zostaje pobrany i przetworzony.
2. **Indexing:** Pozyskany tekst jest czyszczony, dzielony na kontekstowe *chunks* i wektoryzowany.
3. **Storage:** Wygenerowane wektory są zapisywane w wektorowej bazie danych **ChromaDB**.
4. **Retrieval & Generation:** Podczas zapytania użytkownika system pobiera z ChromaDB najbardziej odpowiednie *chunks* i przekazuje je jako kontekst do modelu LLM, który generuje finalną odpowiedź.

## Tech Stack
- **Język programowania:** Python 3.14
- **Orkiestracja AI:** LangChain
- **Wektorowa baza danych:** ChromaDB
- **Modele LLM (API):** OpenAI GPT-4o / Meta Llama 3
- **Web scraping / parsowanie:** Requests, BeautifulSoup4
- **Backend:** FastAPI
- **Frontend:** Streamlit
