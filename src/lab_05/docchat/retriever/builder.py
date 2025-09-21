import sys

# Fix SQLite version compatibility for ChromaDB
try:
    import pysqlite3.dbapi2 as sqlite3

    sys.modules["sqlite3"] = sqlite3
except ImportError:
    pass  # Use system sqlite3 if pysqlite3 not available

import logging
import os

from dotenv import load_dotenv
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings

from config.settings import settings

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class RetrieverBuilder:
    def __init__(self):
        """Initialize the retriever builder with Azure OpenAI embeddings."""
        # Azure OpenAI embedding configuration
        azure_embedding = AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            chunk_size=1000,  # Adjust based on your needs
        )
        self.embeddings = azure_embedding

    def build_hybrid_retriever(self, docs):
        """Build a hybrid retriever using BM25 and vector-based retrieval."""
        try:
            # Ensure all docs are proper Document objects with required attributes
            import os
            import shutil

            from langchain.schema import Document

            processed_docs = []
            for doc in docs:
                if isinstance(doc, Document):
                    # Ensure the document has proper metadata
                    if not hasattr(doc, "metadata") or doc.metadata is None:
                        doc.metadata = {}
                    processed_docs.append(doc)
                else:
                    # Convert to proper Document if it's not already
                    if hasattr(doc, "page_content"):
                        content = doc.page_content
                        metadata = getattr(doc, "metadata", {})
                    else:
                        content = str(doc)
                        metadata = {}
                    processed_docs.append(
                        Document(page_content=content, metadata=metadata)
                    )

            logger.info(f"Processed {len(processed_docs)} documents for retriever")

            # Create BM25 retriever
            bm25 = BM25Retriever.from_documents(processed_docs)
            bm25.k = settings.VECTOR_SEARCH_K  # Set the number of documents to retrieve
            logger.info("BM25 retriever created successfully.")

            # Handle ChromaDB corruption by cleaning up if needed
            try:
                # Create Chroma vector store
                vector_store = Chroma.from_documents(
                    documents=processed_docs,
                    embedding=self.embeddings,
                    persist_directory=settings.CHROMA_DB_PATH,
                )
                logger.info("Vector store created successfully.")
            except Exception as chroma_error:
                if "'_type'" in str(chroma_error):
                    logger.warning(
                        "ChromaDB corruption detected, cleaning up and retrying..."
                    )
                    if os.path.exists(settings.CHROMA_DB_PATH):
                        shutil.rmtree(settings.CHROMA_DB_PATH)
                        logger.info(
                            f"Cleaned up corrupted ChromaDB at {settings.CHROMA_DB_PATH}"
                        )

                    # Retry creating vector store
                    vector_store = Chroma.from_documents(
                        documents=processed_docs,
                        embedding=self.embeddings,
                        persist_directory=settings.CHROMA_DB_PATH,
                    )
                    logger.info("Vector store created successfully after cleanup.")
                else:
                    raise chroma_error

            # Create vector-based retriever
            vector_retriever = vector_store.as_retriever(
                search_kwargs={"k": settings.VECTOR_SEARCH_K}
            )
            logger.info("Vector retriever created successfully.")

            # Combine retrievers into a hybrid retriever
            hybrid_retriever = EnsembleRetriever(
                retrievers=[bm25, vector_retriever],
                weights=settings.HYBRID_RETRIEVER_WEIGHTS,
            )
            logger.info("Hybrid retriever created successfully.")
            return hybrid_retriever
        except Exception as e:
            logger.error(f"Failed to build hybrid retriever: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
