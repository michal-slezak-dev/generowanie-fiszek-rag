# WikiCard AI – Generator Fiszek z Wikipedii
**Projekt zaliczeniowy z przedmiotu Programowanie w Językach Funkcyjnych (PJF)**  
**Autor:** Michał Ślęzak, WCY23IJ2S1, nr albumu 860 65  
**Prowadzący laboratorium:** mgr inż. Piotr Bączyk  

WikiCard AI to aplikacja generująca fiszki edukacyjne na podstawie stron z Wikipedii. Wykorzystuje **RAG (Retrieval-Augmented Generation)** do wyszukiwania kluczowych fragmentów tekstu i tworzenia merytorycznych fiszek. Dodatkowy algorytm **SM-2** optymalizuje proces nauki poprzez rozłożone powtórki - oblicza optymalny interwał między sesjami.

---
## Funkcjonalności
- **Pipeline RAG:** Automatyczne pobieranie treści ze strony Wikipedii po wklejeniu URL, chunking, indeksowanie do ChromaDB i generowanie fiszek przez model LLM.
- **Baza wektorowa:** ChromaDB do semantycznego wyszukiwania kontekstu.
- **Trwałe przechowywanie:** SQLite do zapisywania decku fiszek, stanu nauki oraz możliwość usunięcia danego decku fiszek.
- **System powtórek SM-2:** Oblicza interwały i ease factor na podstawie oceny danej fiszki przez użytkownika.
---

## Stos technologiczny
| Kategoria | Technologie |
|-----------|-------------|
| **Język** | Python 3.13.9 |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **AI** | LangChain, Meta Llama 3.1 (Ollama) |
| **Wektorowa baza danych** | ChromaDB |
| **Baza danych** | SQLite |
---

## Działanie
### Pipeline RAG
1. **Ingestion:** Pobieranie HTML z Wikipedii.
2. **Indexing:** Podział na chunki, wektoryzacja.
3. **Storage:** Zapis do ChromaDB.
4. **Retrieval + Generation:** Wyszukiwanie podobnych chunków i generowanie fiszek do formatu JSON przez model Llama 3.1.

### Algorytm SM-2
Na podstawie oceny fiszki aktualizuje:
- **Easiness Factor (EF)**
- **Interval** (dni do powtórki)
- **Repetitions** (licznik sukcesów)
---

## Uruchomienie
### Wymagania
- Ollama z modelem: `ollama pull llama3.1`
- Python 3.13.9+

### Instalacja 
```bash
git clone https://github.com/michal-slezak-dev/generowanie-fiszek-rag.git
cd generowanie-fiszek-rag
pip install -r requirements.txt
```

### Start
Wykonujemy te komendy z folderu głównego generowanie-fiszek-rag poprzez dwa terminale.

Terminal 1 - backend:
```bash
cd backend
uvicorn main:app --reload
```

Terminal 2 - frontend:
```bash
streamlit run frontend/Home.py
```
