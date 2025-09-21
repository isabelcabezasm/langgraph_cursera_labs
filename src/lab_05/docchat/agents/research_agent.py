from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from typing import Dict, List
from langchain.schema import Document
from config.settings import settings
import json
import os

# Azure AI setup - these should be configured in your environment variables or settings
azure_base_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
# use GPT-4o (or GPT-4-turbo) — These models are ideal for generating grounded, 
# high-quality responses based on retrieved content in a Retrieval-Augmented Generation (RAG) pipeline. 
# instead "meta-llama/llama-3-2-90b-vision-instruct", 
azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") 

# Build full endpoint URL for Azure AI Inference
azure_endpoint = f"{azure_base_endpoint}openai/deployments/{azure_deployment_name}"

# Only initialize client if all required variables are present
client = None
if azure_base_endpoint and azure_api_key and azure_deployment_name:
    client = ChatCompletionsClient(
        endpoint=azure_endpoint,
        credential=AzureKeyCredential(azure_api_key)
    )


class ResearchAgent:
    def __init__(self):
        """
        Initialize the research agent with the Azure AI client.
        """
        # Initialize the Azure AI client
        if client is None:
            raise ValueError("Azure AI client not initialized. Please check your environment variables.")
        print("Initializing ResearchAgent with Azure AI...")
        self.client = client
        self.deployment_name = azure_deployment_name
        print("Azure AI client initialized successfully.")

    def sanitize_response(self, response_text: str) -> str:
        """
        Sanitize the LLM's response by stripping unnecessary whitespace.
        """
        return response_text.strip()

    def generate_prompt(self, question: str, context: str) -> str:
        """
        Generate a structured prompt for the LLM to generate a precise and factual answer.
        """
        prompt = f"""
        **Instructions:**
        - Answer the following question using only the provided context.
        - Be clear, concise, and factual.
        - Return as much information as you can get from the context.
        
        **Question:** {question}
        **Context:**
        {context}

        **Provide your answer below:**
        """
        return prompt

    def generate(self, question: str, documents: List[Document]) -> Dict:
        """
        Generate an initial answer using the provided documents.
        """
        print(f"ResearchAgent.generate called with question='{question}' and {len(documents)} documents.")

        # Combine the top document contents into one string
        context = "\n\n".join([doc.page_content for doc in documents])
        print(f"Combined context length: {len(context)} characters.")

        # Create a prompt for the LLM
        prompt = self.generate_prompt(question, context)
        print("Prompt created for the LLM.")

        # Call the Azure AI model to generate the answer
        try:
            print("Sending prompt to the model...")
            response = self.client.complete(
                messages=[
                    SystemMessage(content="You are an AI assistant designed to provide precise and factual answers based on the given context."),
                    UserMessage(content=prompt)
                ],
                model=self.deployment_name,
                temperature=0.3,
                max_tokens=300
            )
            print("LLM response received.")
        except Exception as e:
            print(f"Error during model inference: {e}")
            raise RuntimeError("Failed to generate answer due to a model error.") from e

        # Extract and process the Azure AI response
        try:
            llm_response = response.choices[0].message.content.strip()
            print(f"Raw LLM response:\n{llm_response}")
        except (AttributeError, IndexError) as e:
            print(f"Unexpected response structure: {e}")
            llm_response = "I cannot answer this question based on the provided documents."

        # Sanitize the response
        draft_answer = self.sanitize_response(llm_response) if llm_response else "I cannot answer this question based on the provided documents."

        print(f"Generated answer: {draft_answer}")

        return {
            "draft_answer": draft_answer,
            "context_used": context
        }