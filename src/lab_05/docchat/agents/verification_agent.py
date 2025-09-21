import json  # Import for JSON serialization
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from typing import Dict, List
from langchain.schema import Document
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure AI setup - these should be configured in your environment variables or settings
azure_base_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
# GPT-4o or GPT-4-turbo These models are ideal for evaluating the consistency and groundedness of 
# generated answers against retrieved documents. They support structured prompting and can be used in evaluation pipelines.
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

class VerificationAgent:
    def __init__(self):
        """
        Initialize the verification agent with the Azure AI client.
        """
        # Initialize the Azure AI client
        if client is None:
            raise ValueError("Azure AI client not initialized. Please check your environment variables.")
        print("Initializing VerificationAgent with Azure AI...")
        self.client = client
        self.deployment_name = azure_deployment_name
        print("Azure AI client initialized successfully.")

    def sanitize_response(self, response_text: str) -> str:
        """
        Sanitize the LLM's response by stripping unnecessary whitespace.
        """
        return response_text.strip()

    def generate_prompt(self, answer: str, context: str) -> str:
        """
        Generate a structured prompt for the LLM to verify the answer against the context.
        """
        prompt = f"""
        **Instructions:**
        - Verify the following answer against the provided context.
        - Check for:
        1. Direct/indirect factual support (YES/NO)
        2. Unsupported claims (list any if present)
        3. Contradictions (list any if present)
        4. Relevance to the question (YES/NO)
        - Provide additional details or explanations where relevant.
        - Respond in the exact format specified below without adding any unrelated information.

        **Format:**
        Supported: YES/NO
        Unsupported Claims: [item1, item2, ...]
        Contradictions: [item1, item2, ...]
        Relevant: YES/NO
        Additional Details: [Any extra information or explanations]

        **Answer:** {answer}
        **Context:**
        {context}

        **Respond ONLY with the above format.**
        """
        return prompt

    def parse_verification_response(self, response_text: str) -> Dict:
        """
        Parse the LLM's verification response into a structured dictionary.
        """
        try:
            lines = response_text.split('\n')
            verification = {}
            valid_keys_found = 0
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Normalize key to match expected format
                    if key.lower() == "supported":
                        final_key = "Supported"
                        valid_keys_found += 1
                    elif key.lower() == "unsupported claims":
                        final_key = "Unsupported Claims"
                        valid_keys_found += 1
                    elif key.lower() == "contradictions":
                        final_key = "Contradictions"
                        valid_keys_found += 1
                    elif key.lower() == "relevant":
                        final_key = "Relevant"
                        valid_keys_found += 1
                    elif key.lower() == "additional details":
                        final_key = "Additional Details"
                        valid_keys_found += 1
                    else:
                        continue  # Skip unknown keys
                    
                    if final_key in {"Unsupported Claims", "Contradictions"}:
                        # Convert string list to actual list
                        if value.startswith('[') and value.endswith(']'):
                            items = value[1:-1].split(',')
                            # Remove any surrounding quotes and whitespace
                            items = [item.strip().strip('"').strip("'") for item in items if item.strip()]
                            verification[final_key] = items
                        else:
                            verification[final_key] = []
                    elif final_key == "Additional Details":
                        verification[final_key] = value
                    else:
                        verification[final_key] = value.upper()
            
            # If no valid keys were found, return None (malformed response)
            if valid_keys_found == 0:
                return None
            
            # Ensure all keys are present
            for key in ["Supported", "Unsupported Claims", "Contradictions", "Relevant", "Additional Details"]:
                if key not in verification:
                    if key in {"Unsupported Claims", "Contradictions"}:
                        verification[key] = []
                    elif key == "Additional Details":
                        verification[key] = ""
                    else:
                        verification[key] = "NO"

            return verification
        except Exception as e:
            print(f"Error parsing verification response: {e}")
            return None

    def format_verification_report(self, verification: Dict) -> str:
        """
        Format the verification report dictionary into a readable paragraph.
        """
        supported = verification.get("Supported", "NO")
        unsupported_claims = verification.get("Unsupported Claims", [])
        contradictions = verification.get("Contradictions", [])
        relevant = verification.get("Relevant", "NO")
        additional_details = verification.get("Additional Details", "")

        report = f"**Supported:** {supported}\n"
        if unsupported_claims:
            report += f"**Unsupported Claims:** {', '.join(unsupported_claims)}\n"
        else:
            report += f"**Unsupported Claims:** None\n"

        if contradictions:
            report += f"**Contradictions:** {', '.join(contradictions)}\n"
        else:
            report += f"**Contradictions:** None\n"

        report += f"**Relevant:** {relevant}\n"

        if additional_details:
            report += f"**Additional Details:** {additional_details}\n"
        else:
            report += f"**Additional Details:** None\n"

        return report

    def check(self, answer: str, documents: List[Document]) -> Dict:
        """
        Verify the answer against the provided documents.
        """
        print(f"VerificationAgent.check called with answer='{answer}' and {len(documents)} documents.")

        # Combine all document contents into one string without truncation
        context = "\n\n".join([doc.page_content for doc in documents])
        print(f"Combined context length: {len(context)} characters.")

        # Create a prompt for the LLM to verify the answer
        prompt = self.generate_prompt(answer, context)
        print("Prompt created for the LLM.")

        # Call the Azure AI model to generate the verification report
        try:
            print("Sending prompt to the model...")
            response = self.client.complete(
                messages=[
                    SystemMessage(content="You are an AI assistant designed to verify the accuracy and relevance of answers based on the provided context."),
                    UserMessage(content=prompt)
                ],
                model=self.deployment_name,
                temperature=0.0,
                max_tokens=200
            )
            print("LLM response received.")
        except Exception as e:
            print(f"Error during model inference: {e}")
            raise RuntimeError("Failed to verify answer due to a model error.") from e

        # Extract and process the Azure AI response
        try:
            llm_response = response.choices[0].message.content.strip()
            print(f"Raw LLM response:\n{llm_response}")
        except (AttributeError, IndexError) as e:
            print(f"Unexpected response structure: {e}")
            verification_report = {
                "Supported": "NO",
                "Unsupported Claims": [],
                "Contradictions": [],
                "Relevant": "NO",
                "Additional Details": "Invalid response structure from the model."
            }
            verification_report_formatted = self.format_verification_report(verification_report)
            print(f"Verification report:\n{verification_report_formatted}")
            print(f"Context used: {context}")
            return {
                "verification_report": verification_report_formatted,
                "context_used": context
            }

        # Sanitize the response
        sanitized_response = self.sanitize_response(llm_response) if llm_response else ""
        if not sanitized_response:
            print("LLM returned an empty response.")
            verification_report = {
                "Supported": "NO",
                "Unsupported Claims": [],
                "Contradictions": [],
                "Relevant": "NO",
                "Additional Details": "Empty response from the model."
            }
        else:
            # Parse the response into the expected format
            verification_report = self.parse_verification_response(sanitized_response)
            if verification_report is None:
                print("LLM did not respond with the expected format. Using default verification report.")
                verification_report = {
                    "Supported": "NO",
                    "Unsupported Claims": [],
                    "Contradictions": [],
                    "Relevant": "NO",
                    "Additional Details": "Failed to parse the model's response."
                }

        # Format the verification report into a paragraph
        verification_report_formatted = self.format_verification_report(verification_report)
        print(f"Verification report:\n{verification_report_formatted}")
        print(f"Context used: {context}")

        return {
            "verification_report": verification_report_formatted,
            "context_used": context
        }