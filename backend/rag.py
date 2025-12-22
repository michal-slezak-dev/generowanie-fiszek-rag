from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class FlashcardSchema(BaseModel):
    front : str = Field(description="This is the front of the flashcard (question)")
    back : str = Field(description="This is the back of the flashcard (answer)")

class FlashcardDeckSchema(BaseModel):
    cards : List[FlashcardSchema] = Field(description="This is our list of 5 flashcards")

class RAGService:
    def __init__(self, persist_directory : str = "./chroma_db", model_name : str = 'llama3.1'):
        # self.llm_model = llm_model
        # self.embedding_model = embedding_model
        self.model_name = model_name
        self.persist_directory = persist_directory

        # Initialize embedding and LLM
        self.embedding_function = OllamaEmbeddings(model=self.model_name)
        self.llm = ChatOllama(model=self.model_name, temperature=0.1)

        # Vector store 
        # self.vector_store = None
        # self.retriever = None
        # self.chain = None 

    def scrape_and_load(self, url : str) -> List[Any]:
        """Scrapes and loads the content of our Wikipedia page"""
        if "wikipedia.org" not in url:
            raise ValueError("URL must be from wikipedia.org")
        
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            return docs
        except Exception as e:
            raise ValueError(f"Could not load the URL: {url}. Error {e}")
    
    def chunk_documents(self, docs : List[Any], chunk_size : int = 1000, chunk_overlap : int = 200) -> List[Any]:
        """Divides the conent of our Wikipedia page into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap
        )

        splits = text_splitter.split_documents(docs)
        return splits
    
    def index_documents(self, chunks : List[Any], collection_name : str) -> Chroma: # vectorization
        """Vectorizes our chunks"""
        # if self.vector_store:
        #     self.vector_store.delete_collection()

        self.delete_collection(collection_name) 

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_function,
            collection_name=collection_name,
            persist_directory=self.persist_directory
        )

        return vector_store
    

        # self.retriever = self.vector_store.as_retriever()
        # self._create_chain()

        # return len(splits)

    def generate_flashcards(self, collection_name : str, topic : str = "Create 5 flashcards about this wikipedia page") -> List[Dict[str, str]]:
            """Generates our list of flashcards"""
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embedding_function,
                persist_directory=self.persist_directory
            )

            retriever = vector_store.as_retriever(search_kwargs = {'k': 5}) # top 5 answers, the closest
            context_docs = retriever.invoke("important facts definitions concepts summary")
            context_text = format_docs(context_docs)

            parser = JsonOutputParser(pydantic_object=FlashcardDeckSchema)
            
            # template = """
            #         ROLE:
            #         You are an academic knowledge assistant. Your mission is to transform raw text (Wikipedia data) into high-quality pedagogical materials (flashcards).

            #         TASK:
            #         Analyze the provided context and generate flashcards optimized for spaced repetition based on the user's request. Everytime, try to generate different flashcards.

            #         GOALS:
            #         1. Extract core definitions, core information, and scientific concepts.
            #         2. Focus on single, atomic facts for better memory retention.
            #         3. Use precise, objective academic language.
            #         4. Output strictly as a JSON object following the format instructions below.

            #         CONTEXT (SOURCE MATERIAL):
            #         {context}

            #         RULES:
            #         - Do NOT add information that is not present in the CONTEXT documents.
            #         - IGNORE metadata like edit dates, licensing info, or source citations, etc.
            #         - If facts are missing, do not invent information.
            #         - NO conversational fillers (e.g., {{"Here are your flashcards"}} etc.). Output ONLY the JSON.

            #         FORMAT INSTRUCTIONS:
            #         {format_instructions}

            #         USER REQUEST:
            #         {topic}
            #         """
            # prompt = ChatPromptTemplate.from_template(template)

            prompt = ChatPromptTemplate.from_messages([
                (
                    "system", """
                    ROLE:
                    You are an academic knowledge assistant. Your mission is to transform raw text (Wikipedia data) into high-quality pedagogical materials (flashcards).

                    GOALS:
                    1. Extract core definitions, core information, and scientific concepts.
                    2. Focus on single, atomic facts for better memory retention.
                    3. Use precise, objective academic language.
                    4. Output strictly as a JSON object following the format instructions below.

                    RULES:
                    - Do NOT add information that is not present in the CONTEXT documents.
                    - IGNORE metadata like edit dates, licensing info, or source citations, etc.
                    - If facts are missing, do not invent information.
                    - NO conversational fillers (e.g., {{"Here are your flashcards"}} etc.). Output ONLY the JSON.

                    FORMAT INSTRUCTIONS:
                    {format_instructions}
                """),
                ("user","""
                    TASK:
                    Analyze the provided context and generate flashcards optimized for spaced repetition based on the user's request. Everytime, try to generate different flashcards.
                 
                 
                    CONTEXT (SOURCE MATERIAL):
                    {context}

                    

                    USER REQUEST:
                    {topic}
                """)
            ])

            chain = prompt | self.llm | parser

            try:
                response = chain.invoke({
                    'context' : context_text,
                    'topic' : topic,
                    'format_instructions' : parser.get_format_instructions()
                })

                return response.get('cards', [])
            except Exception as e:
                print(f'Error generation flashcards : {e}')
                return []
            
    def delete_collection(self, collection_name : str):
        """Deletes our list of flascards - our deck if the user clicks Regenerate - One of our core functions"""
        try:
            vector_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embedding_function,
                persist_directory=self.persist_directory
            )

            vector_store.delete_collection()
            print(f"Collection {collection_name} successfully deleted")
        except Exception as e:
            print(f"Failed to delete the collection / the collection does not exist: {e}")


    def process_and_ask(self, url: str) -> List[Dict[str, str]]:
        """Test function - testing the workflow"""
        collection_name = "wiki_data"
        
        print(f"Loading {url}...")
        docs = self.scrape_and_load(url)
        
        chunks = self.chunk_documents(docs)
        
        print("Indexing...")
        self.index_documents(chunks, collection_name)
        
        print("Generating flashcards...")
        flashcards = self.generate_flashcards(collection_name)
        
        return flashcards



    
    # def _create_chain(self):
    #     template = """
    #             ROLE:
    #             You are an academic knowledge assistant. Your mission is to transform raw text (Wikipedia data) into high-quality pedagogical materials (flashcards).

    #             TASK:
    #             Analyze the provided context and generate flashcards optimized for spaced repetition based on the user's request. Everytime, try to generate different flashcards.

    #             GOALS:
    #             1. Extract core definitions, core information, and scientific concepts.
    #             2. Focus on single, atomic facts for better memory retention.
    #             3. Use precise, objective academic language.
    #             4. Output strictly as a JSON object (list of dictionaries with {{"question": "answer"}}).

    #             CONTEXT (SOURCE MATERIAL):
    #             {context}

    #             RULES:
    #             - Do NOT add information that is not present in the CONTEXT documents.
    #             - IGNORE metadata like edit dates, licensing info, or source citations, etc.
    #             - If facts are missing, do not invent information.
    #             - NO conversational fillers (e.g., {{"Here are your flashcards"}} etc.). Output ONLY the JSON.

    #             USER REQUEST:
    #             {question}
    #             """
        
    #     prompt = ChatPromptTemplate.from_template(template)

    #     def format_docs(docs):
    #         return "\n\n".join(doc.page_content for doc in docs)

    #     self.chain = (
    #         {'context': self.retriever | format_docs, 'question' : RunnablePassthrough()}
    #         | prompt
    #         | self.llm
    #         | StrOutputParser()
    #     )
    
    # def ask_question(self, question : str) -> str:
    #     if not self.chain:
    #         return "Please process a ..."
    #     return self.chain.invoke(question)
    
# test
# rag_server = RAGService()                   
# rag_server.process_url("https://en.wikipedia.org/wiki/Python_(programming_language)")
# answer = rag_server.ask_question("Create 5 flashcards about this wikipedia page")
# print(answer)


rag = RAGService()
cards = rag.process_and_ask("https://en.wikipedia.org/wiki/Python_(programming_language)")

import json
print(json.dumps(cards, indent=2))

