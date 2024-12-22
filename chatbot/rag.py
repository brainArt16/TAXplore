import os
import logging
from typing import List
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoherePDFRAG:
    def __init__(self, api_key: str = None, prompt_text: str = None):
        self._api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self._api_key:
            raise ValueError(
                "Cohere API Key must be provided or set in the environment."
            )
        self._embedding = None
        self._llm = None
        self._prompt_text = (
            prompt_text
            or """
            You are an AI assistant for a company that offers specialized services to its customers. Your goal is to provide accurate and concise answers based on the given context and chat history. Follow these guidelines:

            1. Use the provided context and chat history to formulate your response.
            2. Ensure your answer is clear, concise, and directly related to the provided context.
            3. If the question is not relevant to the provided context, respond with: "I'm sorry, but I can only answer questions related to the provided context. Please provide more information or ask a related question."
            
            Context: {context}
            Chat History: {history}
            Question: {question}
        """
        )
        self._prompt = None

    @property
    def embedding(self):
        if not self._embedding:
            self._embedding = CohereEmbeddings(cohere_api_key=self.api_key)
        return self._embedding

    @property
    def llm(self):
        if not self._llm:
            self._llm = ChatCohere(cohere_api_key=self.api_key)
        return self._llm

    def get_prompt(self, custom_template: str = None):
        """Initialize or update the prompt."""
        if not self._prompt or custom_template:
            template = custom_template or self._prompt_text
            self._prompt = PromptTemplate(
                input_variables=["context", "history", "question"],
                output_variables=["answer"],
                template=template,
            )
        return self._prompt

    def load_documents(self, document_path: str) -> List:
        """Load documents from a PDF file.  
        Args:
            document_path: Path to the PDF file.
        Returns:
            List of documents loaded from the PDF file.
        """
        try:
            loader = PyPDFLoader(document_path)
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} documents from {document_path}")
            return documents
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
            raise

    @staticmethod
    def split_text(
        documents: List, chunk_size: int = 1000, chunk_overlap: int = 100
    ) -> List:
        """Split the text into chunks.
        Args:
            documents: List of documents to split.
            chunk_size: Size of each chunk.
            chunk_overlap: Overlap between chunks.
        Returns:
            List of split text chunks.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        texts = splitter.split_documents(documents)
        logger.info(f"Split documents into {len(texts)} chunks")
        return texts

    def create_vectorstore(self, texts: List, collection_name: str):
        """Create and persist a vectorstore from the provided texts.
        Args:
            texts: List of texts to create the vectorstore.
            collection_name: Name of the collection to store the vectorstore.
        """
        try:
            vectorstore = FAISS.from_documents(
                documents=texts,
                embedding=self.embedding,
                collection_name=collection_name,
            )
            vectorstore.persist()
            logger.info(
                f"Vectorstore created and persisted with collection name: {collection_name}"
            )
        except Exception as e:
            logger.error(f"Failed to create vectorstore: {e}")
            raise

    def load_vectorstore(self, collection_name: str) -> FAISS:
        """Load the vectorstore from the provided collection name.
        Args:
            collection_name: Name of the collection to load the vectorstore.
        Returns:
            Loaded vectorstore.
        """
        try:
            vectorstore = FAISS(
                embedding_function=self.embedding,
                collection_name=collection_name,
            )
            logger.info(f"Loaded vectorstore with collection name: {collection_name}")
            return vectorstore
        except Exception as e:
            logger.error(f"Failed to load vectorstore: {e}")
            raise

    def create_chain(self, vectorstore: FAISS) -> RetrievalQA:
        """Create a retrieval chain with the provided vectorstore.
        Args:
            vectorstore: Vectorstore to use for retrieval.
        Returns:
            RetrievalQA chain.
        """
        memory = ConversationBufferMemory(memory_key="history", input_key="question")
        try:
            retriever = MultiQueryRetriever.from_llm(
                retriever=vectorstore.as_retriever(),
                llm=self.llm,
            )
            chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=retriever,
                chain_type="stuff",
                chain_type_kwargs={"prompt": self.prompt, "memory": memory},
            )
            logger.info("Retrieval chain created successfully")
            return chain
        except Exception as e:
            logger.error(f"Failed to create chain: {e}")
            raise

    def get_answer(self, chain: RetrievalQA, question: str) -> str:
        """Get the answer to the provided question.
        Args:
            chain: RetrievalQA chain.
            question: Question to answer.   
        Returns:
            Answer to the question.
        """
        try:
            answer = chain.invoke(question)
            logger.info(f"Answer retrieved: {answer}")
            return answer
        except Exception as e:
            logger.error(f"Failed to retrieve answer: {e}")
            raise
