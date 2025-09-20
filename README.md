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


## Lab 02: Building a Reflection Agent with LangGraph

The `lab02_reflection_agent.ipynb` notebook demonstrates how to build a sophisticated reflection agent using LangGraph and Azure OpenAI. This lab showcases advanced AI capabilities where the agent can evaluate and improve its own outputs through iterative reflection cycles.

**Note:** This implementation uses StateGraph instead of MessageGraph, which was deprecated in LangGraph version 1.0.0. All code has been updated to use the current best practices.

### Features
- **Self-improving AI system:** Agent generates content, critiques it, and refines through multiple iterations
- **Reflection-based workflow:** Implements a dual-system approach (quick generation + thoughtful reflection)
- **LinkedIn content generation:** Specialized for creating professional LinkedIn posts with optimal engagement
- **State management:** Uses TypedDict with StateGraph for robust conversation state handling
- **Azure OpenAI integration:** Leverages Azure ChatOpenAI for intelligent content generation and critique
- **Conditional routing:** Smart workflow control based on iteration count and quality assessment
- **Graph visualization:** Visual representation of the reflection workflow using pygraphviz

### Workflow Architecture
The reflection agent implements a sophisticated workflow with the following components:

#### Workflow Nodes
- **Generation Node:** Creates initial LinkedIn post content based on user requirements
- **Reflection Node:** Critically evaluates generated content and provides detailed feedback
- **Router Function:** Determines whether to continue reflection cycles or end the workflow

#### Reflection Process
1. **Initial Generation:** Quick, instinctive response to user prompt
2. **Critical Evaluation:** Professional content strategist assessment of quality, engagement potential, and LinkedIn best practices
3. **Iterative Refinement:** Multiple cycles of improvement based on structured feedback
4. **Quality Control:** Automatic termination after optimal number of iterations (typically 3 cycles)

### Workflow Flow
1. `START` → `Generate` (create initial LinkedIn post)
2. `Generate` → `Reflect` (critique and provide improvement suggestions)
3. `Reflect` → `Generate` (refine content based on feedback)
4. **Repeat steps 2-3** until quality threshold is met or maximum iterations reached
5. `Generate` → `END` (finalize optimized content)

### Key Improvements from MessageGraph to StateGraph
- **Enhanced State Management:** More robust state handling with TypedDict structure
- **Better Type Safety:** Improved type checking and state validation
- **Cleaner API:** Simplified node function signatures and state updates
- **Future-Proof:** Uses current LangGraph best practices and stable APIs

### Reflection Criteria
The agent evaluates content based on:
- **Professional Quality:** Alignment with LinkedIn standards and best practices
- **Engagement Potential:** Likelihood to generate likes, comments, and shares
- **Structure & Clarity:** Readability, formatting, and message clarity
- **Industry Relevance:** Appropriateness for target audience and current trends
- **Call-to-Action Effectiveness:** Strength of engagement prompts and takeaways

### Example Usage
**Input:** "Write a LinkedIn post on getting a software developer job at IBM under 160 characters"

**Process:**
1. **Initial Generation:** Basic post creation
2. **First Reflection:** Critique focusing on engagement and professionalism
3. **Second Generation:** Refined post incorporating feedback
4. **Final Reflection:** Polish and optimize for maximum impact
5. **Final Output:** Professional, engaging LinkedIn post ready for publication

### Azure OpenAI Configuration
- **Model:** `gpt-4o-mini` (configurable deployment)
- **Temperature:** 0.7 for balanced creativity and consistency
- **Max tokens:** 1024 for comprehensive responses
- **Request timeout:** 120 seconds
- **Top-p:** 0.95 for diverse, high-quality outputs


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
