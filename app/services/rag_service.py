import os
import json
from dotenv import load_dotenv

load_dotenv()

if not os.getenv('USER_AGENT'):
    os.environ['USER_AGENT'] = 'WikiQuizAI/1.0'

CHROMA_PERSIST_DIR = "./chroma_db_data"
OLLAMA_MODEL = "llama3.1"

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import PydanticOutputParser

from app.core.models import Flashcard, FlashcardList


class RAGService:
    def __init__(self):
        # Ollama - wektoryzacja
        self.embeddings_model = OllamaEmbeddings(model=OLLAMA_MODEL)

        # Ollama model
        self.llm = ChatOllama(model=OLLAMA_MODEL, format="json")

        # inicjowanie chunkera
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        # model dla wyjscia
        self.parser = PydanticOutputParser(pydantic_object=FlashcardList)

        print(f"RAGService zainicjalizowany. Uzywa Ollama ({OLLAMA_MODEL}). Gotowy do dzialania!")

    def ingest_url(self, url: str) -> None:
        """
        Pobiera tresc z danego URL, tnie na chunki, wektoryzuje i zapisuje
        do lokalnej bazy wektorowej ChromaDB.
        """
        print(f"\nLadowanie tresci z URL: {url} ---")
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
        except Exception as e:
            print(f"Blad ladowania URL: {e}")
            return

        print(f"Ciecie dokumentu na chunki ---")
        texts = self.text_splitter.split_documents(documents)
        print(f"Utworzono {len(texts)} chunkow.")

        print(f"Wektorowanie i zapis do ChromaDB ---")
        vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings_model,
            persist_directory=CHROMA_PERSIST_DIR
        )

        vector_store.persist()

        print(f"Ingestowanie zakonczone! ---")
        print(f"Wektory zapisano w folderze: {CHROMA_PERSIST_DIR}")

    def generate_quiz(self, query: str, num_questions: int = 5) -> list[Flashcard]:
        # inicjalizacja ChromaDB
        print(f"\nLadowanie bazy ChromaDB i wyszukiwanie kontekstu dla: {query} ---")
        try:
            vector_store = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=self.embeddings_model
            )
            retriever = vector_store.as_retriever(search_kwargs={"k": 5}) # bedzie szukal 5 najbarziej podobnych fragmentow
        except Exception as e:
            print(f"Blad ladowania ChromaDB: {e}")
            return []

        # wyszukiwanie kontekstu, retrieval
        docs = retriever.invoke(query)
        context = "\n".join([d.page_content for d in docs])

        # prompt!
        print("Wywolywanie modelu Ollama i generowanie fiszek (5)... ---")

        # pobieram instrukcje
        format_instructions = self.parser.get_format_instructions()

        system_content = (
            "Jesteś ekspertem w generowaniu fiszek. Twoim zadaniem jest stworzenie "
            f"zestawu {num_questions} fiszek (Pytanie-Odpowiedź) na podstawie kontekstu z Wikipedii, nie uwzgledniaj informacji z sekcji z linkami. "
            
            "ODPOWIEDŹ MUSI ZAWIERAĆ WYŁĄCZNIE CZYSTY JSON. "
            "NIE WOLNO dodawać żadnych dodatkowych komentarzy, wstępów, podsumowań, "
            "ani otaczającego tekstu typu 'Oto Twoja odpowiedź:'."
            "ZACZNIJ I ZAKOŃCZ TYLKO kodem JSON."
            
            "Musisz zwrócić odpowiedź w formacie JSON zgodnym z tą instrukcją: \n"
            "{format_instructions}"
        )

        human_content = (
            f"Użyj następującego kontekstu, aby stworzyć {num_questions} fiszek na temat: {query}\n\n"
            "KONTEKST: {context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_content),
                ("human", human_content),
            ]
        )

        formatted_prompt = prompt.format_messages(
            context=context,
            query=query,
            format_instructions=format_instructions
        )

        json_string = ""

        try:
            # model LLM
            response = self.llm.invoke(formatted_prompt)
            json_string = response.content

            # PARSOWANIE I ZWROT WYNIKU
            parsed_object = self.parser.parse(json_string)
            final_quiz = parsed_object.flashcards

            print("Generacja i parsowanie zakonczone!")
            return final_quiz
        except Exception as e:
            print(f"Blad generacji: {e}")
