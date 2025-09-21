# LangGraph Coursera Labs

This repository contains the Azure version of the lab exercises from the Coursera course [Agentic AI with LangChain and LangGraph](https://www.coursera.org/learn/agentic-ai-with-langchain-and-langgraph/).

To improve my skills, I'm replicating the exercises using Azure.

## Project Structure

```
├── .devcontainer/          # Development container configuration
├── src/
│   └── notebooks/          # Jupyter notebooks with lab exercises
│       ├── lab01_01_check_credentials.ipynb     # Authentication Workflow with LangGraph
│       ├── lab01_02_chatbot.ipynb     # Q&A Chatbot with Context-Aware Responses
│       ├── lab02_reflection_agent.ipynb        # Self-Improving Content Generation Agent
│       ├── lab03_01_reflexion_agent.ipynb      # Reflection Agent with External Knowledge Integration (Tavily)
│       ├── lab04_01_example_ReAct.ipynb        # ReAct Pattern Implementation with Tool Calling
│       ├── lab04_02_exercise_01_ReAct_calculator.ipynb # Exercise: Build a Calculator Tool
│       ├── lab04_03_exercise_02_ReAct_news_summary.ipynb # Exercise: Create a News Summary Tool
│       └── lab_05/            # Advanced document chat application
│           └── docchat/       # Multi-agent document analysis system
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


## Lab 03: Building a Reflection Agent with External Knowledge Integration

The `lab03_01_reflexion_agent.ipynb` notebook demonstrates how to build an advanced reflection agent that combines self-evaluation capabilities with external knowledge retrieval. This lab represents a significant evolution in AI agent architecture, integrating real-time web search to enhance the quality and accuracy of generated responses.

**Note:** This implementation has been fully migrated from the deprecated MessageGraph to StateGraph, incorporating all the latest LangGraph v1.0+ best practices and modern state management patterns.

### Features
- **External Knowledge Integration:** Real-time web search using Tavily Search API for up-to-date information
- **Advanced Reflection Workflow:** Multi-stage process combining initial response generation, external research, and evidence-based revision
- **Specialized Medical/Nutrition Personas:** Implements distinct AI personas (Dr. Paul Saladino's carnivore approach vs. Dr. David Attia's evidence-based medicine)
- **Tool-Enhanced AI:** Structured tool calling for automated web searches based on generated queries
- **Evidence-Based Revision:** Automatic incorporation of peer-reviewed research and scientific literature
- **StateGraph Architecture:** Modern LangGraph implementation with robust state management
- **Citation Management:** Automatic reference collection and formatting for academic rigor

### Workflow Architecture
The lab implements a sophisticated three-node workflow with external knowledge integration:

#### Core Components
- **AgentState:** TypedDict-based state management with message history and metadata
- **Structured Tool Calling:** Pydantic models for reliable AI-tool communication
- **External Search Integration:** Tavily API for real-time web knowledge retrieval
- **Conditional Iteration Control:** Smart routing based on research depth and iteration count

#### Workflow Nodes
- **Respond Node:** Generates initial draft responses using internal knowledge and structured output
- **Execute Tools Node:** Processes search queries and retrieves external knowledge from the web
- **Revisor Node:** Synthesizes external research with internal knowledge for evidence-based refinement

#### State Management Enhancements
- **Message Accumulation:** Proper handling of conversation history with `add_messages` reducer
- **Tool Message Integration:** Seamless incorporation of external search results into the conversation flow
- **Iteration Tracking:** Automatic counting of research cycles for optimal workflow control

### Workflow Flow
1. `START` → `Respond` (generate initial answer with search queries)
2. `Respond` → `Execute Tools` (perform web searches based on generated queries)
3. `Execute Tools` → `Revisor` (synthesize research into improved response)
4. `Revisor` → `Execute Tools` (conditional: continue research if needed)
5. **Repeat steps 3-4** until research threshold is met (MAX_ITERATIONS = 4)
6. `Revisor` → `END` (finalize evidence-based response)

### External Knowledge Integration
The agent leverages the Tavily Search API to:
- **Generate Research Queries:** AI automatically creates targeted search queries based on content gaps
- **Retrieve Current Information:** Access real-time web content including recent studies and publications
- **Validate Claims:** Cross-reference generated content with authoritative sources
- **Enhance Accuracy:** Incorporate up-to-date data that may not be in the AI's training data

### Advanced Persona Implementation
The lab showcases two distinct AI personalities:

#### Initial Responder: Dr. Paul Saladino (Carnivore MD)
- **Focus:** Animal-based nutrition advocacy and plant compound skepticism
- **Approach:** Evolutionary biology perspective on human nutrition
- **Specialization:** Carnivore elimination protocols and organ meat benefits

#### Revisor: Dr. David Attia (Evidence-Based Medicine)
- **Focus:** Rigorous scientific methodology and clinical research integration
- **Approach:** Mechanistic understanding with individual variability consideration
- **Specialization:** Biomarker analysis, RCT interpretation, and evidence grading

### Key Technical Improvements (MessageGraph → StateGraph)
- **Enhanced Type Safety:** Full TypedDict implementation with proper type annotations
- **Improved State Flow:** Cleaner message handling with automatic state updates
- **Modern API Usage:** Adoption of current LangGraph patterns and stable interfaces
- **Better Error Handling:** Robust state validation and graceful failure recovery
- **Tool Integration:** Streamlined external API integration with proper state management

### Structured Output Models
The lab implements sophisticated Pydantic models for reliable AI communication:

```python
class Reflection(BaseModel):
    missing: str = Field(description="What information is missing")
    superfluous: str = Field(description="What information is unnecessary")

class AnswerQuestion(BaseModel):
    answer: str = Field(description="Main response to the question")
    reflection: Reflection = Field(description="Self-critique of the answer")
    search_queries: List[str] = Field(description="Queries for additional research")

class ReviseAnswer(AnswerQuestion):
    references: List[str] = Field(description="Citations motivating your updated answer")
```

### Research Integration Process
1. **Query Generation:** AI analyzes response gaps and generates targeted search queries
2. **External Search:** Tavily API retrieves relevant web content and research papers
3. **Knowledge Synthesis:** Revisor integrates external findings with internal knowledge
4. **Citation Management:** Automatic reference formatting and source attribution
5. **Quality Control:** Evidence-based validation and claim substantiation

### Example Workflow
**Input:** "I'm pre-diabetic and need to lower my blood sugar, and I have heart issues. What breakfast foods should I eat and avoid?"

**Process:**
1. **Initial Response:** Dr. Saladino persona generates carnivore-focused breakfast recommendations
2. **Research Phase:** Automated searches for "antinutrients in plant foods," "bioavailability studies," etc.
3. **Evidence Integration:** Dr. Attia persona incorporates peer-reviewed research and clinical evidence
4. **Citation Addition:** Proper reference formatting with numerical citations
5. **Final Output:** Comprehensive, evidence-based breakfast recommendations with scientific backing

### External API Configuration
**Tavily Search Integration:**
- Real-time web search capabilities
- Academic paper and research study access
- Configurable result limits for focused research
- JSON-formatted search results for easy AI processing

### Azure OpenAI Configuration
- **Model:** `gpt-4o-mini` (configurable deployment)
- **Temperature:** 0.7 for balanced creativity and factual accuracy
- **Max tokens:** 1024 for comprehensive responses
- **Request timeout:** 120 seconds
- **Retry logic:** 3 attempts for improved reliability
- **Top-p:** 0.95 for diverse, high-quality outputs


## Lab 04: Building a ReAct Agent with Tool Calling

The `lab04_01_example_ReAct.ipynb` notebook demonstrates how to implement the **ReAct (Reasoning and Acting)** pattern using LangGraph and Azure OpenAI. This lab showcases how AI agents can reason about problems and take actions using external tools in an iterative process.

**Note:** This implementation uses StateGraph with modern LangGraph v1.0+ patterns, demonstrating both manual ReAct execution for understanding and automated graph-based implementation for production use.

### Features
- **ReAct Pattern Implementation:** Classic Reasoning and Acting methodology where agents think, act, and observe iteratively
- **Multi-Tool Integration:** Combines web search (Tavily) and domain-specific tools (clothing recommendation)
- **Manual Execution Walkthrough:** Step-by-step demonstration of ReAct flow for educational purposes
- **Automated Graph Workflow:** Production-ready implementation using LangGraph's StateGraph
- **Tool Calling Framework:** Structured tool registration and execution with proper state management
- **Conditional Routing:** Smart decision-making between continued tool use and workflow completion
- **Azure OpenAI Integration:** Leverages Azure ChatOpenAI with tool binding capabilities
- **Graph Visualization:** Visual representation of the ReAct workflow using pygraphviz

### ReAct Pattern Overview
The ReAct pattern enables AI agents to:
1. **Reason:** Analyze the problem and determine what information is needed
2. **Act:** Execute appropriate tools to gather required information
3. **Observe:** Process tool results and integrate them into the reasoning process
4. **Iterate:** Repeat the cycle until the task is complete

### Tool Implementation
The lab implements two complementary tools:

#### Tool 1: Web Search (Tavily API)
- **Purpose:** Real-time web information retrieval
- **Use Cases:** Current weather, news, facts, and general knowledge queries
- **Integration:** Tavily Search API for reliable web content access

#### Tool 2: Clothing Recommendation
- **Purpose:** Weather-based clothing suggestions
- **Logic:** Keyword-based analysis of weather descriptions
- **Recommendations:** Contextual advice for different weather conditions (snow, rain, heat, cold)

### Workflow Architecture
The lab demonstrates both manual and automated ReAct implementations:

#### Manual ReAct Execution (Educational)
**Step-by-Step Process:**
1. **Initial Query Processing:** User question analyzed and initial response generated
2. **Tool Execution:** Identified tools called with appropriate parameters
3. **Result Processing:** Tool outputs integrated into agent state
4. **Next Action Decision:** Determine if additional tools are needed
5. **Final Response Generation:** Synthesize all information into comprehensive answer

#### Automated Graph Implementation (Production)
**Workflow Nodes:**
- **Agent Node (`call_model`):** Processes conversation state and generates responses with tool calls
- **Tools Node (`tool_node`):** Executes all pending tool calls and returns results
- **Router Function (`should_continue`):** Conditional logic determining workflow continuation

**State Management:**
- **AgentState:** TypedDict with message history using `add_messages` reducer
- **Tool Registry:** Centralized tool management with name-based lookup
- **Message Flow:** Proper handling of HumanMessage, AIMessage, and ToolMessage types

### Workflow Flow (Automated)
1. `START` → `Agent` (process user query and determine tool needs)
2. `Agent` → `Tools` (execute required tools if any tool calls exist)
3. `Tools` → `Agent` (return tool results and re-evaluate)
4. **Repeat steps 2-3** until no more tools are needed
5. `Agent` → `END` (provide final comprehensive response)

### Key Technical Implementations

#### Tool Registration Pattern
```python
tools = [search_tool, recommend_clothing]
tools_by_name = {tool.name: tool for tool in tools}
```

#### State Management with Reducers
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

#### Conditional Routing Logic
```python
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
```

### Example Workflow Execution
**Input:** "What's the weather like in Zurich, and what should I wear based on the temperature?"

**Process:**
1. **Reasoning:** Agent determines it needs current weather information for Zurich
2. **Action 1:** Executes web search for Zurich weather conditions
3. **Observation 1:** Processes weather data (temperature, conditions)
4. **Reasoning:** Agent determines clothing recommendation is needed based on weather
5. **Action 2:** Executes clothing recommendation tool with weather description
6. **Observation 2:** Receives appropriate clothing suggestions
7. **Final Response:** Synthesizes weather information with clothing recommendations

### Educational Benefits
- **ReAct Pattern Understanding:** Clear demonstration of reasoning-action cycles
- **Manual vs. Automated:** Comparison between step-by-step execution and graph automation
- **Tool Integration:** Best practices for multi-tool agent development
- **State Management:** Modern LangGraph patterns for conversation state handling
- **Conditional Logic:** Implementation of decision-making in agent workflows

### Azure OpenAI Configuration
- **Model:** `gpt-4o-mini` (configurable deployment)
- **Temperature:** 0.7 for balanced reasoning and creativity
- **Tool Binding:** Direct tool binding to LLM for structured tool calling
- **Max tokens:** 1024 for comprehensive responses
- **Request timeout:** 120 seconds
- **Retry logic:** 3 attempts for improved reliability
- **Top-p:** 0.95 for diverse, high-quality outputs

### Production Considerations
- **Error Handling:** Robust tool execution with proper exception management
- **Tool Registry:** Scalable pattern for adding new tools to the agent
- **Message History:** Complete conversation context preservation
- **Graph Compilation:** Optimized workflow execution with LangGraph's compiled graphs
- **Streaming Support:** Real-time response streaming for better user experience
- **Microsoft Ecosystem:** Better integration with other Microsoft AI services
- **Reliability:** Enterprise-grade infrastructure and uptime guarantees
- **SafeSearch:** Built-in content filtering and safety controls


## Lab 04.1: Building a Calculator Tool Exercise

The `lab04_02_exercise_01_ReAct_calculator.ipynb` notebook provides a hands-on exercise for building a secure mathematical calculator tool that integrates with the ReAct agent workflow. This exercise demonstrates how to create custom tools that can handle complex mathematical operations safely.

### Features
- **Safe Mathematical Evaluation:** Uses Python's AST (Abstract Syntax Tree) module instead of dangerous `eval()` for secure expression parsing
- **Comprehensive Math Functions:** Supports basic arithmetic, trigonometry (sin, cos, tan), logarithms (log, log10), exponentials, and mathematical constants (π, e)
- **Robust Error Handling:** Graceful handling of invalid expressions and unsupported operations
- **Manual and Automated Execution:** Demonstrates both step-by-step manual ReAct execution and automated graph-based workflow
- **Tool Integration:** Seamless integration with LangGraph's StateGraph architecture

### Mathematical Capabilities
- **Basic Operations:** Addition, subtraction, multiplication, division, exponentiation
- **Advanced Functions:** sqrt, sin, cos, tan, log, log10, exp, abs
- **Constants:** π (pi), e (Euler's number)
- **Complex Expressions:** Supports nested operations like "15% of 250 plus the square root of 144"

### Example Usage
**Input:** "What's 15% of 250 plus the square root of 144?"

**Process:**
1. **Reasoning:** Agent identifies need for mathematical calculation
2. **Action:** Calls calculator_tool with expression "0.15 * 250 + sqrt(144)"
3. **Observation:** Receives result "49.5"
4. **Response:** Provides formatted answer with explanation


## Lab 04.2: Building a News Summarization Tool Exercise

The `lab04_03_exercise_02_ReAct_news_summary.ipynb` notebook provides a hands-on exercise for creating a news summarization tool that works with web search functionality. This exercise demonstrates how to build tools that process and format external data for enhanced AI responses.

### Features
- **Multi-Format Processing:** Handles both JSON-formatted search results and plain text content
- **Intelligent Content Extraction:** Automatically extracts titles, URLs, and key information from news articles
- **Professional Formatting:** Creates visually appealing summaries with emojis and structured layout
- **Article Limitation:** Processes top 3 articles for focused, digestible summaries
- **Error Handling:** Robust error management for malformed data and processing failures
- **Search Integration:** Works seamlessly with Tavily Search API for real-time news retrieval

### Summary Format
The tool generates professional summaries with:
```
📊 **NEWS SUMMARY**
==================================================

📰 **Article Title**
🔗 URL Link
📝 **Summary:** Key points extracted from article content...
```

### Example Usage
**Input:** "Find recent AI news and summarize the top 3 articles"

**Process:**
1. **Reasoning:** Agent identifies need for current news information
2. **Action 1:** Executes search_tool with query "recent AI news"
3. **Observation 1:** Receives search results with multiple articles
4. **Action 2:** Calls news_summarizer_tool with search results
5. **Observation 2:** Receives formatted summary of top 3 articles
5. **Observation 2:** Receives formatted summary of top 3 articles
6. **Response:** Provides comprehensive news summary with titles, links, and key points


## Lab 05: DocChat - Advanced Document Analysis Application

The `src/lab_05/docchat/` directory contains a production-ready document chat application that represents the culmination of LangGraph multi-agent system development. This advanced project demonstrates enterprise-level implementation of document processing, retrieval, and AI-powered question answering.

### Architecture Overview

DocChat implements a sophisticated multi-agent workflow using LangGraph's StateGraph architecture, featuring three specialized agents working in coordination:

#### Agent Architecture
- **Relevance Checker Agent**: Determines if uploaded documents contain information relevant to user queries
- **Research Agent**: Performs intelligent document retrieval and generates comprehensive draft answers
- **Verification Agent**: Validates and fact-checks research findings for accuracy and completeness

#### Workflow Components
- **Document Processor**: Advanced file handling using Docling for PDF, DOCX, TXT, and other formats
- **Hybrid Retriever**: Combines BM25 keyword search with ChromaDB vector embeddings for optimal retrieval
- **State Management**: Robust TypedDict-based workflow state with proper error handling
- **Web Interface**: Professional Gradio-based chat interface with file upload capabilities

### Key Features

#### Multi-Agent Workflow
- **StateGraph Implementation**: Modern LangGraph v1.0+ patterns with conditional routing
- **Agent Coordination**: Intelligent workflow control with decision points for re-research and verification
- **Error Recovery**: Graceful handling of agent failures and malformed responses
- **Iteration Control**: Configurable limits to prevent infinite loops while ensuring thorough analysis

#### Document Processing Capabilities
- **Format Support**: PDF, DOCX, TXT, HTML, and other document formats
- **Intelligent Chunking**: Semantic text splitting optimized for retrieval accuracy
- **Metadata Extraction**: Automatic extraction of document structure and context
- **Caching System**: Efficient document processing with intelligent caching mechanisms

#### Hybrid Retrieval System
- **Vector Search**: ChromaDB with Azure OpenAI embeddings (text-embedding-ada-002)
- **Keyword Search**: BM25 algorithm for exact term matching and traditional IR
- **Ensemble Retrieval**: Intelligent combination of both approaches for optimal results
- **Relevance Scoring**: Advanced scoring mechanisms for result ranking and filtering

#### Azure AI Integration
- **Azure AI Inference**: Complete migration from IBM WatsonX to Azure AI services
- **Azure OpenAI Embeddings**: High-quality text embeddings for semantic search
- **Configurable Models**: Support for various Azure AI models with temperature and token controls
- **Authentication**: Secure Azure credential management and API key handling

#### Modern Development Tools
- **UV Package Manager**: Fast, reliable Python package and project management
- **Dependency Lock Files**: Reproducible builds with `uv.lock` for consistent environments
- **Virtual Environment Management**: Automatic virtual environment creation and activation
- **Fast Installation**: Significantly faster dependency resolution and installation compared to pip

### Technical Implementation

#### Workflow State Management
```python
class AgentState(TypedDict):
    question: str
    documents: List[Document]
    draft_answer: str
    verification_report: str
    is_relevant: bool
    retriever: EnsembleRetriever
```

#### Multi-Agent Coordination
1. **Relevance Check**: Documents analyzed for query relevance before processing
2. **Research Phase**: Hybrid retrieval generates comprehensive draft answers
3. **Verification Phase**: Draft answers validated and enhanced with fact-checking
4. **Decision Logic**: Conditional routing for re-research or completion based on quality metrics

#### Agent Specializations

**Relevance Checker Agent:**
- **Purpose**: Efficient pre-filtering of irrelevant documents
- **Model Configuration**: Temperature 0.0 for consistent decision-making
- **Response Format**: Boolean relevance determination with reasoning
- **Optimization**: Prevents unnecessary processing of irrelevant content

**Research Agent:**
- **Purpose**: Comprehensive document analysis and answer generation
- **Model Configuration**: Temperature 0.3, max_tokens 300 for balanced creativity
- **Retrieval Strategy**: Hybrid search with configurable result limits
- **Output Format**: Structured draft answers with source attribution

**Verification Agent:**
- **Purpose**: Quality assurance and fact validation
- **Model Configuration**: Temperature 0.0, max_tokens 200 for precision
- **Validation Criteria**: Accuracy, completeness, and source verification
- **Enhancement**: Suggestions for answer improvement and re-research triggers

### Deployment and Usage

#### Environment Configuration
```env
# Azure AI Services
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_chat_deployment_name
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME=text-embedding-ada-002
AZURE_OPENAI_API_VERSION=2024-02-01
```

#### Web Interface Features
- **File Upload**: Drag-and-drop document upload with format validation
- **Real-time Chat**: Interactive conversation interface with typing indicators
- **Processing Status**: Visual feedback during document processing and analysis
- **Example Queries**: Pre-configured examples for common use cases
- **Response Formatting**: Professional output with source citations and confidence indicators

#### Example Use Cases

**Google Environmental Report Analysis:**
- **Query**: "Retrieve the data center PUE efficiency values in Singapore 2nd facility in 2019 and 2022"
- **Process**: Multi-agent workflow extracts specific metrics with verification
- **Output**: Precise numerical data with source page references

**Technical Document Analysis:**
- **Query**: "Summarize DeepSeek-R1 model's performance evaluation on coding tasks"
- **Process**: Research agent analyzes technical content, verification ensures accuracy
- **Output**: Comprehensive performance summary with methodology validation

### Advanced Capabilities

#### Production-Ready Features
- **Comprehensive Testing**: 47+ test cases covering all agents and integration scenarios
- **Error Handling**: Robust exception management with graceful degradation
- **Performance Optimization**: Efficient caching and retrieval strategies
- **Scalability**: Modular architecture supporting additional agents and capabilities
- **Monitoring**: Detailed logging and performance metrics

#### SQLite Compatibility
- **ChromaDB Integration**: Automatic SQLite version upgrade for compatibility
- **Version Management**: Seamless handling of SQLite 3.34.1 → 3.46.1 upgrade
- **Fallback Strategy**: Graceful degradation when pysqlite3 unavailable

#### Development Tools
- **Testing Framework**: Pytest-based comprehensive test suite
- **Code Quality**: Black, isort, ruff, and mypy for code standards
- **Documentation**: Extensive inline documentation and type hints
- **Migration Guide**: Complete Azure migration documentation

### Installation and Setup

#### Quick Start
```bash
# Navigate to docchat directory
cd src/lab_05/docchat/

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies using uv
uv sync

# Configure environment
cp template.env .env
# Edit .env with your Azure credentials

# Launch application
uv run python app.py
```

#### Development Setup
```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest integration_tests/ -v

# Code formatting
uv run black .
uv run isort .
uv run ruff check .
```

#### Alternative Setup (using pip)
```bash
# If you prefer using pip instead of uv
cd src/lab_05/docchat/
pip install -r requirements.txt
python app.py
```

### Architecture Benefits

#### Enterprise Readiness
- **Modular Design**: Clear separation of concerns with pluggable components
- **Scalable Architecture**: Support for additional agents and document types
- **Production Deployment**: Docker support and containerization ready
- **Security**: Secure credential management and input validation

#### Educational Value
- **Complete Workflow**: End-to-end multi-agent system implementation
- **Best Practices**: Modern LangGraph patterns and state management
- **Real-world Application**: Production-quality code with comprehensive testing
- **Migration Example**: Demonstrates platform migration strategies (IBM → Azure)
- **Modern Tooling**: Showcases contemporary Python development practices with `uv`

#### Technical Innovation
- **Hybrid Retrieval**: Novel combination of vector and keyword search
- **Agent Coordination**: Advanced multi-agent workflow patterns
- **State Management**: Sophisticated state handling with error recovery
- **Interface Design**: Professional web interface with excellent UX

DocChat represents the culmination of the LangGraph learning journey, demonstrating how multiple concepts from previous labs combine into a cohesive, production-ready application suitable for enterprise document analysis and knowledge extraction workflows.


## Prerequisites

## Prerequisites

- Python 3.11 or newer
- Jupyter Notebook or JupyterLab environment  
- `uv` package manager (for Lab 05) - install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Required packages (installed automatically in the dev container):
    - `langgraph` (version 1.0+)
    - `langchain-openai` (for Azure OpenAI integration)
    - `langchain-community` (for external tool integrations)
    - `python-dotenv` (for environment configuration)
    - `grandalf` (for graph visualization)
    - `matplotlib` (for plotting)
    - `networkx` (for graph operations)
    - `pygraphviz` (for advanced graph visualization)
    - `pydantic` (for structured data validation)
    - `tavily-python` (for external knowledge retrieval in Lab 03 and 04)
    - `gradio` (for Lab 05 web interface)
    - `chromadb` (for Lab 05 vector database)
    - `docling` (for Lab 05 document processing)
    - `azure-ai-inference` (for Lab 05 Azure AI integration)

## Setup

1. Clone this repository.
2. Open it in VS Code using the dev container (recommended).
3. Create a `.env` file with your API credentials:
     ```
     # Azure OpenAI Configuration (required for all labs)
     AZURE_OPENAI_API_KEY=your_azure_api_key_here
     AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
     OPENAI_API_VERSION=your_api_version_here
     
     # Tavily Search API (required for original Lab 03)
     TAVILY_API_KEY=your_tavily_api_key_here
     ```
4. Open and run the notebooks in the `src/notebooks/` directory
5. For Lab 05 DocChat: Navigate to `src/lab_05/docchat/`, run `uv sync` then `uv run python app.py`

### API Key Setup Guide

#### Azure OpenAI (Required for Labs 01.2, 02, 03)
1. Create an Azure OpenAI resource in the Azure Portal
2. Deploy a GPT model (recommended: `gpt-4o-mini`)
3. Copy the API key, endpoint, and API version from the Azure Portal

#### Tavily Search API (Required for Lab 03 and 04)
1. Sign up at [Tavily.com](https://tavily.com/)
2. Create a free account (includes generous free tier)
3. Generate an API key from your dashboard
4. Add the key to your `.env` file

## Visualization

The project includes several visualization options:
- **ASCII diagrams:** Quick workflow understanding for simple graphs
- **Grandalf-based layouts:** Detailed visualization with professional graph rendering
- **Pygraphviz integration:** Advanced graph visualization with customizable layouts and styling
- **Interactive displays:** Notebook-embedded graph visualization for real-time workflow monitoring

## Migration Notes: MessageGraph → StateGraph

**Important:** All labs in this repository have been updated to use StateGraph instead of the deprecated MessageGraph. Key changes include:

### Technical Improvements
- **Enhanced State Management:** TypedDict-based state with proper type safety
- **Modern API Usage:** Current LangGraph v1.0+ patterns and best practices
- **Better Tool Integration:** Streamlined external API integration with robust error handling
- **Improved Message Handling:** Automatic message accumulation with `add_messages` reducer

### Breaking Changes Addressed
- **Import Updates:** `from langgraph.graph import StateGraph` instead of `MessageGraph`
- **State Schema:** All workflows now use proper state definitions with `AgentState(TypedDict)`
- **Node Functions:** Updated to return state dictionaries instead of raw messages
- **Tool Calling:** Enhanced structured output with Pydantic models for reliability

### Benefits of Migration
- **Future-Proof Code:** Uses stable APIs that will be supported long-term
- **Better Performance:** Improved memory management and execution efficiency
- **Enhanced Debugging:** Clearer error messages and state inspection capabilities
- **Scalability:** Better handling of complex workflows and large conversation histories

## Contributing

This is a learning repository. Feel free to experiment with the code and create your own variations of the workflows.

## License

This project is for my personal learning and was created as part of the Coursera LangGraph labs.
