from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class RAGService:
    def __init__(self, llm_model : str = 'llama3', embedding_model : str = 'llama3'):
        self.llm_model = llm_model
        self.embedding_model = embedding_model

        # Initialize embedding and LLM
        self.embeddings = OllamaEmbeddings(model=self.embedding_model)
        self.llm = ChatOllama(model=self.llm_model)

        # Vector store 
        self.vector_store = None
        self.retriever = None
        self.chain = None 

    def process_url(self, url : str):
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
        except:
            raise ValueError(f"Could not load the URL: {url}")

        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )

        splits = text_splitter.split_documents(docs)
    

        if self.vector_store:
            self.vector_store.delete_collection()
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            collection_name='current_doc'
        )
    
        self.retriever = self.vector_store.as_retriever()
        self._create_chain()

        return len(splits)
    
    # 
    def _create_chain(self):
        template = """
                ROLE:
                You are an academic knowledge assistant. Your mission is to transform raw text (Wikipedia data) into high-quality pedagogical materials (flashcards).

                TASK:
                Analyze the provided context and generate flashcards optimized for spaced repetition based on the user's request.

                GOALS:
                1. Extract core definitions, core information, and scientific concepts.
                2. Focus on single, atomic facts for better memory retention.
                3. Use precise, objective academic language.
                4. Output strictly as a JSON object (list of dictionaries with "question" and "answer").

                CONTEXT (SOURCE MATERIAL):
                {context}

                RULES:
                - Do NOT add information that is not present in the CONTEXT documents.
                - IGNORE metadata like edit dates, licensing info, or source citations, etc.
                - If facts are missing, do not invent information.
                - NO conversational fillers (e.g., "Here are your flashcards" etc.). Output ONLY the JSON.

                USER REQUEST:
                {question}
                """
        
        prompt = ChatPromptTemplate(template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.chain = (
            {'context': self.retriever | format_docs, "question" : RunnablePassthorugh()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def ask_question(self, question : str) -> str:
        if not self.chain:
            return "Please process a ..."
        return self.chain.invoke(question)
    

rag_server = RAGService()

