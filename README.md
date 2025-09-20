# LangGraph Coursera Labs

Azure-adapted lab exercises from the Coursera course [Agentic AI with LangChain and LangGraph](https://www.coursera.org/learn/agentic-ai-with-langchain-and-langgraph/).

## Labs Overview

### Lab 01.1: Authentication Workflow
Basic stateful authentication workflow using LangGraph with input validation, retry logic, and conditional routing.

### Lab 01.2: Context-Aware Chatbot  
Q&A chatbot that provides different responses based on available context, with Azure OpenAI integration.

### Lab 02: Reflection Agent
Self-improving AI agent that generates content, critiques it, and refines through iterative reflection cycles. Specialized for LinkedIn content generation.

### Lab 03: Reflection Agent with External Knowledge (3 variants)

**Original (`lab03_01_reflexion_agent.ipynb`)**
Uses Tavily Search API for real-time web search and external knowledge integration.

**Bing Search (`lab03_02_reflexion_agent_using_bing_websearch.ipynb`)**  
Azure Bing Search integration with native Microsoft ecosystem support.

**LangChain Bing (`lab03_03_reflexion_agent_using_langchain_tool_bing_search.ipynb`)**
Uses LangChain's standardized Bing Search tools for consistent interface patterns.

All Lab 03 variants implement the same AI agent with different search providers for external knowledge retrieval.

### Lab 04: ReAct Agent with Tool Calling
Implementation of the ReAct (Reasoning and Acting) pattern with multi-tool integration. Demonstrates both manual step-by-step execution and automated graph-based workflow using Tavily search and clothing recommendation tools.

## Quick Setup

1. Clone repository and open in VS Code dev container
2. Copy `template.env` to `.env` and add your API keys:
   ```
   AZURE_OPENAI_API_KEY=your_key
   AZURE_OPENAI_ENDPOINT=your_endpoint  
   OPENAI_API_VERSION=2024-12-01-preview
   TAVILY_API_KEY=your_tavily_key        # For original Lab 03
   BING_SEARCH_API_KEY=your_bing_key     # For Bing variants
   ```
3. Run notebooks in `src/notebooks/`

## API Keys Required

- **Azure OpenAI**: All labs except 01.1
- **Tavily Search**: Original Lab 03 and Lab 04
- **Bing Search**: Lab 03 Bing variants only

## Notes

- All labs updated to use StateGraph (LangGraph v1.0+)
- Dev container includes all required dependencies
- Choose Lab 03 variant based on your preferred search provider