# WikiQuiz AI: Intelligent Flashcard & Quiz Generator
Przedmiot: Programowanie w Językach Funkcyjnych\
Autor: Michał Ślęzak WCY23IJ2S1 860 65\
Prowadzący laboratorium: mgr inż. Piotr Bączyk


## Opis Projektu

**WikiQuiz AI** to projekt zaliczeniowy z przedmiotu PJF stworzony w Pythonie, która automatyzuje proces nauki poprzez generowanie spersonalizowanych quizów i fiszek bezpośrednio z artykułów Wikipedii z wykorzystaniem RAG.

## Planowane, kluczowe funkcjonalności (w zależności od czasu...)

| Kategoria | Funkcjonalność | Opis                                                                                                                |
| :--- | :--- |:--------------------------------------------------------------------------------------------------------------------|
| **Generowanie** | RAG Pipeline | Wykorzystanie LangChain i ChromaDB do kontekstowego generowania pytań na podstawie wyszukanych fragmentów tekstu.   |
| **Baza Wiedzy** | Wektorowa Baza Danych | Indeksowanie tekstu z URL Wikipedii w **ChromaDB** w celu szybkiego wyszukiwania.                                   |
| **Trwałość Danych** | **Zapis Stanu (SQL)** | Użycie tradycyjnej relacyjnej bazy danych (np. SQLite/PostgreSQL) do **trwałego przechowywania wygenerowanych fiszek** oraz ich stanów nauki (dane SM-2). |
| **Uczenie** | Algorytm SM-2 (SRS) | Implementacja algorytmu SuperMemo-2 w Pythonie, który oblicza optymalny interwał powtórek dla każdej fiszki.        |
| **Modularność** | Architektura OOP | Organizacja kodu w warstwy i klasy późniejszej rozbudowy o FastAPI.                                                 |

### Pipeline RAG (Retrieval-Augmented Generation)

1.  **Ingestion:** Użytkownik podaje URL.
2.  **Indexing:** Tekst jest dzielony na kontekstowe *chunks* i jest wektoryzowany.
3.  **Storage:** Wektory są zapisywane w bazie wektorowej **ChromaDB**.
4.  **Generation:** Zapytanie użytkownika trafia do LLM, któremu podany jest *kontekst* (oraz najbardziej relewantne *chunks* pobrane z ChromaDB).

## Tech Stack
* **Język:** Python 3.14
* **Orkiestracja AI:** LangChain
* **Wektorowa Baza Danych:** ChromaDB
* **API LLM:** OpenAI (GPT-4o) / Llama3
* **Parsowanie:** BeautifulSoup4, Requests
* **Backend/Frontend:** FastAPI / Streamlit