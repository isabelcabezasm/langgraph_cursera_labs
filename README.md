# LangGraph Coursera Labs

This repository contains lab exercises and projects for learning LangGraph - Building Stateful AI Workflows.

## Project Structure

```
├── .devcontainer/          # Development container configuration
├── src/
│   └── notebooks/          # Jupyter notebooks with lab exercises
│       ├── lab01.ipynb     # Authentication Workflow with LangGraph
│       └── lab - LangGraph101 Building Stateful AI Workflows.ipynb
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Lab 01: Authentication Workflow

The `lab01.ipynb` notebook demonstrates how to build a stateful authentication workflow using LangGraph. The workflow includes:

### Features
- **State Management**: Using TypedDict for maintaining authentication state
- **Node-based Architecture**: Separate nodes for input, validation, success, and failure handling
- **Conditional Routing**: Smart routing based on authentication results
- **Retry Logic**: Automatic retry loop for failed authentication attempts
- **Visualization**: Graph visualization using both ASCII diagrams and grandalf library

### Workflow Nodes
- **Input Node**: Collects username and password from user
- **Validate Node**: Checks credentials against expected values
- **Success Node**: Handles successful authentication
- **Failure Node**: Handles failed authentication with retry option
- **Router Node**: Conditional routing based on authentication state

### Workflow Flow
1. `START` → `Input` (collect credentials)
2. `Input` → `Validate` (check authentication)
3. `Validate` → `Success` OR `Failure` (conditional based on auth result)
4. `Success` → `END` (successful login)
5. `Failure` → `Input` (retry authentication)

### Valid Credentials
- Username: `isa`
- Password: `secure_password123`

## Prerequisites

- Python 3.11+
- Jupyter Notebook environment
- Required packages (installed automatically in dev container):
  - `langgraph`
  - `langchain-openai`
  - `python-dotenv`
  - `grandalf` (for graph visualization)
  - `matplotlib` (for plotting)
  - `networkx` (for graph operations)

## Setup

1. Clone this repository
2. Open in VS Code with the dev container (recommended)
3. Create a `.env` file with your Azure OpenAI credentials (if needed for certain exercises):
   ```
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   OPENAI_API_VERSION=your_api_version_here
   ```
4. Open and run the notebooks in the `src/notebooks/` directory

## Learning Objectives

- Understand LangGraph's StateGraph architecture
- Learn to build stateful AI workflows
- Practice implementing conditional logic in graph-based systems
- Explore graph visualization techniques
- Master state management in AI applications

## Visualization

The project includes multiple visualization approaches:
- ASCII diagrams for quick understanding
- Grandalf-based graph layouts for detailed visualization
- Mermaid diagrams (when available)

## Contributing

This is a learning repository. Feel free to experiment with the code and create your own variations of the workflows.

## License

This project is for educational purposes as part of Coursera LangGraph learning labs.