import logging
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

logger = logging.getLogger(__name__)

# Azure AI setup - these should be configured in your environment variables or settings
azure_base_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_deployment_name = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT_NAME"
)  # use Gpt4 or gpt4-turbo here, instead of ibm/granite-3-8b-instruct

# Build full endpoint URL for Azure AI Inference
azure_endpoint = f"{azure_base_endpoint}openai/deployments/{azure_deployment_name}"

# Only initialize client if all required variables are present
client = None
if azure_base_endpoint and azure_api_key and azure_deployment_name:
    client = ChatCompletionsClient(
        endpoint=azure_endpoint, credential=AzureKeyCredential(azure_api_key)
    )


class RelevanceChecker:
    def __init__(self):
        # Initialize the Azure AI client
        if client is None:
            raise ValueError(
                "Azure AI client not initialized. Please check your environment variables."
            )
        self.client = client
        self.deployment_name = azure_deployment_name

    def check(self, question: str, retriever, k=3) -> str:
        """
        1. Retrieve the top-k document chunks from the global retriever.
        2. Combine them into a single text string.
        3. Pass that text + question to the LLM for classification.

        Returns: "CAN_ANSWER", "PARTIAL", or "NO_MATCH".
        """

        logger.debug(
            f"RelevanceChecker.check called with question='{question}' and k={k}"
        )

        # Retrieve doc chunks from the ensemble retriever
        top_docs = retriever.invoke(question)
        if not top_docs:
            logger.debug(
                "No documents returned from retriever.invoke(). Classifying as NO_MATCH."
            )
            return "NO_MATCH"

        # Combine the top k chunk texts into one string
        document_content = "\n\n".join(doc.page_content for doc in top_docs[:k])

        # Create a prompt for the LLM to classify relevance
        prompt = f"""
        **Instructions:**
        - Classify how well the document content addresses the user's question.
        - Respond with only one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH.
        - Do not include any additional text or explanation.

        **Labels:**
        1) "CAN_ANSWER": The passages contain enough explicit information to fully answer the question.
        2) "PARTIAL": The passages mention or discuss the question's topic but do not provide all the details needed for a complete answer.
        3) "NO_MATCH": The passages do not discuss or mention the question's topic at all.

        **Important:** If the passages mention or reference the topic or timeframe of the question in any way, even if incomplete, respond with "PARTIAL" instead of "NO_MATCH".

        **Question:** {question}
        **Passages:** {document_content}

        **Respond ONLY with one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH**
        """

        # Call the Azure AI model
        try:
            response = self.client.complete(
                messages=[
                    SystemMessage(
                        content="You are an AI relevance checker between a user's question and provided document content."
                    ),
                    UserMessage(content=prompt),
                ],
                model=self.deployment_name,
                temperature=0,
                max_tokens=10,
            )
        except Exception as e:
            logger.error(f"Error during model inference: {e}")
            return "NO_MATCH"

        # Extract the content from the Azure AI response
        try:
            llm_response = response.choices[0].message.content.strip().upper()
            logger.debug(f"LLM response: {llm_response}")
        except (AttributeError, IndexError) as e:
            logger.error(f"Unexpected response structure: {e}")
            return "NO_MATCH"

        print(f"Checker response: {llm_response}")

        # Validate the response
        valid_labels = {"CAN_ANSWER", "PARTIAL", "NO_MATCH"}
        if llm_response not in valid_labels:
            logger.debug("LLM did not respond with a valid label. Forcing 'NO_MATCH'.")
            classification = "NO_MATCH"
        else:
            logger.debug(f"Classification recognized as '{llm_response}'.")
            classification = llm_response

        return classification
