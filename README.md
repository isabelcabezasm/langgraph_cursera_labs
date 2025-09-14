# LangGraph Coursera Labs

This repository contains the Azure version of the lab exercises from the Coursera course [Agentic AI with LangChain and LangGraph](https://www.coursera.org/learn/agentic-ai-with-langchain-and-langgraph/).

To improve my skills, I'm replicating the exercises using Azure.

## Project Structure

```
├── .devcontainer/          # Development container configuration
├── src/
│   └── notebooks/          # Jupyter notebooks with lab exercises
│       ├── lab01_01_check_credentials.ipynb     # Authentication Workflow with LangGraph
│       └── lab01_02_chatbot.ipynb     # Q&A Chatbot with Context-Aware Responses
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Lab 01.1: Authentication Workflow

The `lab01_01_check_credentials.ipynb` notebook demonstrates how to build a stateful authentication workflow using LangGraph. The workflow includes:

### Features
- **State management:** Using TypedDict to maintain authentication state.
- **Node-based architecture:** Separate nodes for input, validation, success, and failure handling.
- **Conditional routing:** Smart routing based on authentication results.
- **Retry logic:** Automatic retry loop for failed authentication attempts.
- **Visualization:** Graph visualization using both ASCII diagrams and the Grandalf library.

### Workflow Nodes
- **Input Node:** Collects username and password from the user.
- **Validate Node:** Checks credentials against expected values.
- **Success Node:** Handles successful authentication.
- **Failure Node:** Handles failed authentication and provides a retry option.
- **Router Node:** Performs conditional routing based on authentication state.

### Workflow Flow
1. `START` → `Input` (collect credentials)
2. `Input` → `Validate` (check authentication)
3. `Validate` → `Success` OR `Failure` (conditional based on auth result)
4. `Success` → `END` (successful login)
5. `Failure` → `Input` (retry authentication)

## Lab 01.2: Q&A Chatbot with Context-Aware Responses

The `lab01_02_chatbot.ipynb` notebook demonstrates how to build a context-aware Q&A chatbot using LangGraph and Azure OpenAI. This lab showcases:

### Features
- **Context-aware responses:** The chatbot provides different responses based on available context
- **Question processing:** Input validation and question handling
- **Dynamic context provision:** Context is provided only for relevant questions
- **Azure OpenAI integration:** Uses Azure ChatOpenAI for generating intelligent responses
- **Graceful fallbacks:** Handles questions without context appropriately

### Workflow Nodes
- **Input Node:** Processes and validates the incoming question
- **Context Provider Node:** Determines if context is available for the question (currently supports LangGraph-related questions)
- **Answer Node:** Generates responses using Azure OpenAI, incorporating context when available

### Workflow Flow
1. `START` → `Input` (process question)
2. `Input` → `ContextProvider` (check for relevant context)
3. `ContextProvider` → `Answer` (generate response with or without context)
4. `Answer` → `END` (return final answer)

### Example Usage
- **Question with context:** "What is LangGraph?" → Provides detailed answer using available context
- **Question without context:** "What's the weather like?" → Returns appropriate fallback response

### Azure OpenAI Configuration
The notebook uses Azure OpenAI with the following configuration:
- Model: `gpt-4o-mini` (configurable)
- Temperature: 0.7 for balanced creativity
- Max tokens: 1024
- Request timeout: 120 seconds
- Top-p: 0.95 for diverse responses

## Prerequisites

- Python 3.11 or newer
- Jupyter Notebook or JupyterLab environment
- Required packages (installed automatically in the dev container):
    - `langgraph`
    - `langchain-openai` (for Azure OpenAI integration)
    - `python-dotenv`
    - `grandalf` (for graph visualization)
    - `matplotlib` (for plotting)
    - `networkx` (for graph operations)

## Setup

1. Clone this repository.
2. Open it in VS Code using the dev container (recommended).
3. Create a `.env` file with your Azure OpenAI credentials (required for the chatbot lab):
     ```
     AZURE_OPENAI_API_KEY=your_api_key_here
     AZURE_OPENAI_ENDPOINT=your_endpoint_here
     OPENAI_API_VERSION=your_api_version_here
     ```
4. Open and run the notebooks in the `src/notebooks/` directory.

## Visualization

The project includes several visualization options:
- ASCII diagrams for quick understanding
- Grandalf-based graph layouts for detailed visualization

## Contributing

This is a learning repository. Feel free to experiment with the code and create your own variations of the workflows.

## License

This project is for my personal learning and was created as part of the Coursera LangGraph labs.
