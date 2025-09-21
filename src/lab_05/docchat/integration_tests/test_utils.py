"""
Test utilities and fixtures for agent integration tests.
"""
import os
from typing import List
from langchain.schema import Document

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, rely on environment variables being set
    pass

class TestData:
    """Sample test data for agent testing."""
    
    # Sample documents for testing
    SAMPLE_DOCUMENTS = [
        Document(
            page_content="""
            Azure OpenAI Service provides REST API access to OpenAI's powerful language models including 
            the GPT-4, GPT-4 Turbo with Vision, GPT-3.5-Turbo, and Embeddings model series. These models 
            can be easily adapted to your specific task including but not limited to content generation, 
            summarization, image understanding, semantic search, and natural language to code translation.
            """,
            metadata={"source": "azure_openai_docs.txt", "page": 1}
        ),
        Document(
            page_content="""
            The text-embedding-ada-002 model is OpenAI's second generation embedding model. It replaces 
            16 first-generation embedding models and is more capable, cost-effective, and simpler to use. 
            The new model has 1536 dimensions and is trained on diverse text data. It excels at various 
            text similarity tasks and can be used for search, clustering, recommendations, anomaly detection, 
            diversity measurement, and classification.
            """,
            metadata={"source": "embedding_model_docs.txt", "page": 1}
        ),
        Document(
            page_content="""
            Machine learning is a subset of artificial intelligence (AI) that provides systems the ability 
            to automatically learn and improve from experience without being explicitly programmed. Machine 
            learning focuses on the development of computer programs that can access data and use it to learn 
            for themselves. The process of learning begins with observations or data, such as examples, direct 
            experience, or instruction, in order to look for patterns in data.
            """,
            metadata={"source": "ml_basics.txt", "page": 1}
        ),
        Document(
            page_content="""
            Python is a high-level, interpreted programming language with dynamic semantics. Its high-level 
            built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive 
            for Rapid Application Development, as well as for use as a scripting or glue language to connect 
            existing components together. Python's simple, easy to learn syntax emphasizes readability and 
            therefore reduces the cost of program maintenance.
            """,
            metadata={"source": "python_intro.txt", "page": 1}
        )
    ]
    
    # Sample questions for testing
    TEST_QUESTIONS = {
        "azure_openai": "What is Azure OpenAI Service?",
        "embedding_model": "What are the dimensions of the text-embedding-ada-002 model?",
        "machine_learning": "What is machine learning?",
        "python": "What makes Python attractive for development?",
        "unrelated": "What is the weather like today?",
        "partial": "Tell me about AI models"
    }
    
    # Expected answers for verification testing
    EXPECTED_ANSWERS = {
        "azure_openai": "Azure OpenAI Service provides REST API access to OpenAI's powerful language models including GPT-4, GPT-4 Turbo with Vision, GPT-3.5-Turbo, and Embeddings model series for tasks like content generation, summarization, image understanding, semantic search, and natural language to code translation.",
        "embedding_model": "The text-embedding-ada-002 model has 1536 dimensions and is OpenAI's second generation embedding model that excels at various text similarity tasks.",
        "machine_learning": "Machine learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed."
    }

def check_environment_variables() -> bool:
    """Check if all required environment variables are set."""
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

class MockRetriever:
    """Mock retriever for testing purposes."""
    
    def __init__(self, documents: List[Document]):
        self.documents = documents
    
    def invoke(self, query: str) -> List[Document]:
        """Return relevant documents based on simple keyword matching."""
        # If no documents available, return empty list
        if not self.documents:
            return []
            
        relevant_docs = []
        query_lower = query.lower()
        
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            # Simple keyword matching for testing
            if any(word in content_lower for word in query_lower.split()):
                relevant_docs.append(doc)
        
        # Only return at least one document if documents are available
        if not relevant_docs and self.documents:
            relevant_docs = [self.documents[0]]
        
        return relevant_docs[:3]  # Return top 3 matches