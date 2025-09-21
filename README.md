# LangGraph Coursera Labs

Azure-adapted lab exercises from the Coursera course [Agentic AI with LangChain and LangGraph](https://www.coursera.org/learn/agentic-ai-with-langchain-and-langgraph/).

## Labs Overview

### Lab 01.1: Authentication Workflow
Basic stateful authentication workflow using LangGraph with input validation, retry logic, and conditional routing.

### Lab 01.2: Context-Aware Chatbot  
Q&A chatbot that provides different responses based on available context, with Azure OpenAI integration.

### Lab 02: Reflection Agent
Self-improving AI agent that generates content, critiques it, and refines through iterative reflection cycles. Specialized for LinkedIn content generation.

### Lab 03: Reflection Agent with External Knowledge
Uses Tavily Search API for real-time web search and external knowledge integration.

### Lab 04: ReAct Agent with Tool Calling
Implementation of the ReAct (Reasoning and Acting) pattern with multi-tool integration. Demonstrates both manual step-by-step execution and automated graph-based workflow using Tavily search and clothing recommendation tools.

### Lab 04.1: Calculator Tool Exercise
Hands-on exercise building a secure mathematical calculator tool for the ReAct agent. Implements safe expression evaluation using AST parsing to handle complex mathematical operations including trigonometric functions, logarithms, and constants like π and e.

**Example Queries:** "What's 15% of 250 plus the square root of 144?" or "Calculate sin(π/2) + log10(100)"

### Lab 04.2: News Summarization Tool Exercise  
Hands-on exercise creating a news summarization tool that works with web search functionality. Builds upon the ReAct pattern to fetch and intelligently summarize recent news articles with proper formatting and key information extraction.
**Example Queries:** "Find recent AI news and summarize the top 3 articles" or "Search for recent technology developments and give me a summary"

## Quick Setup

1. Clone repository and open in VS Code dev container
2. Copy `template.env` to `.env` and add your API keys:
   ```
   AZURE_OPENAI_API_KEY=your_key
   AZURE_OPENAI_ENDPOINT=your_endpoint  
   OPENAI_API_VERSION=2024-12-01-preview
   TAVILY_API_KEY=your_tavily_key        # For original Lab 03
   ```
3. Run notebooks in `src/notebooks/`

## API Keys Required

- **Azure OpenAI**: All labs except 01.1
   - **Tavily Search**: Lab 03 and Lab 04

- All labs updated to use StateGraph (LangGraph v1.0+)
- Dev container includes all required dependencies
