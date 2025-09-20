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
│       ├── lab03_02_reflexion_agent_using_bing_websearch.ipynb # Reflection Agent with Azure Bing Search
│       ├── lab03_03_reflexion_agent_using_langchain_tool_bing_search.ipynb # Reflection Agent with LangChain Bing Search Tools
│       └── lab04_01_example_ReAct.ipynb        # ReAct Pattern Implementation with Tool Calling
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


## Lab 03 Alternative: Building a Reflection Agent with Azure Bing Search Integration

The `lab03_02_reflexion_agent_using_bing_websearch.ipynb` notebook provides an alternative implementation of Lab 03 that uses **Azure Bing Search** instead of Tavily for external knowledge retrieval. This variant demonstrates how to integrate Microsoft's Bing Search API for real-time web content access.

### Key Differences from Original Lab 03

#### External Knowledge Provider
- **Original:** Tavily Search API for web content retrieval
- **Alternative:** Azure Bing Search v7 API with native Microsoft integration

#### Search Tool Implementation
- **Simplified Architecture:** Direct Azure Bing Search integration without Tavily compatibility layers
- **Native Format:** Returns Bing's natural response structure (`title`, `url`, `snippet`)
- **Azure Ecosystem Integration:** Seamless integration with other Azure services
- **Enterprise-Ready:** Built on Microsoft's enterprise-grade search infrastructure

### Features Specific to Bing Search Variant
- **Azure Cognitive Services Integration:** Uses Azure's unified API management and authentication
- **Native Bing Search Format:** No format conversion required - uses Bing's natural response structure
- **Simplified Configuration:** Single API key setup through Azure Portal
- **Enhanced Error Handling:** Azure-specific error handling and retry logic
- **SafeSearch Integration:** Built-in content filtering using Bing's SafeSearch capabilities

### Workflow Architecture (Bing Search Variant)
The Bing Search implementation maintains the same sophisticated three-node workflow as the original:

#### Core Components
- **AgentState:** Identical TypedDict-based state management
- **bing_search_tool():** Simplified search function using Azure Bing Search API
- **Structured Tool Calling:** Same Pydantic models for reliable AI-tool communication
- **Conditional Iteration Control:** Identical smart routing and iteration management

#### Key Technical Improvements
- **Simplified Search Integration:** Removed Tavily compatibility layers for cleaner code
- **Native Response Format:** Direct use of Bing's response structure without format conversion
- **Reduced Dependencies:** Fewer external packages required
- **Azure-Native Architecture:** Better integration with Azure ecosystem services

### Bing Search Tool Implementation
```python
def bing_search_tool(query: str, max_results: int = 1):
    """
    Azure Bing Web Search tool for LangGraph workflow
    """
    if not bing_client:
        return {"error": "Azure Bing Search not configured"}
    
    try:
        web_data = bing_client.web.search(
            query=query,
            count=max_results,
            safe_search=SafeSearch.moderate
        )
        
        if web_data.web_pages and web_data.web_pages.value:
            results = []
            for page in web_data.web_pages.value[:max_results]:
                results.append({
                    "title": page.name,
                    "url": page.url,
                    "snippet": page.snippet
                })
            return {"results": results, "query": query}
    except Exception as e:
        return {"error": f"Bing search failed: {str(e)}", "query": query}
```

### Setup Requirements (Bing Search Variant)

#### Azure Bing Search v7 Configuration
1. **Create Bing Search Resource:**
   - Go to [Azure Portal](https://portal.azure.com/)
   - Create a new **Bing Search v7** resource
   - Choose your subscription and resource group
   - Select pricing tier (F1 free tier available)

2. **Get API Credentials:**
   - Navigate to "Keys and Endpoint" in your Bing Search resource
   - Copy the API key (Key 1 or Key 2)
   - Default endpoint: `https://api.bing.microsoft.com/`

3. **Environment Configuration:**
   ```env
   # Add to your .env file
   BING_SEARCH_API_KEY=your_bing_search_api_key_here
   ```

#### Required Python Packages
```bash
pip install azure-cognitiveservices-search-websearch
```

### Workflow Flow (Identical to Original)
1. `START` → `Respond` (generate initial answer with search queries)
2. `Respond` → `Execute Tools` (perform Bing searches based on generated queries)
3. `Execute Tools` → `Revisor` (synthesize research into improved response)
4. `Revisor` → `Execute Tools` (conditional: continue research if needed)
5. **Repeat steps 3-4** until research threshold is met (MAX_ITERATIONS = 4)
6. `Revisor` → `END` (finalize evidence-based response)

### Advantages of Bing Search Implementation
- **Enterprise Integration:** Native Azure ecosystem integration
- **Simplified Codebase:** Cleaner implementation without compatibility layers
- **Cost Efficiency:** Competitive pricing with free tier availability


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

### When to Use Which Version
- **Use Tavily Version (`lab03_01_reflexion_agent.ipynb`)** when:
  - You need specialized academic/research content
  - You prefer Tavily's curated search results
  - You're already using Tavily in other projects

- **Use Bing Search Version (`lab03_02_reflexion_agent_using_bing_websearch.ipynb`)** when:
  - You're working within the Azure ecosystem
  - You prefer Microsoft's enterprise-grade services
  - You want simplified setup and maintenance
  - You need SafeSearch content filtering capabilities

Both implementations provide identical AI agent capabilities with different external knowledge providers, allowing you to choose based on your specific requirements and infrastructure preferences.


## Lab 03 LangChain Alternative: Building a Reflection Agent with LangChain Bing Search Tools

The `lab03_03_reflexion_agent_using_langchain_tool_bing_search.ipynb` notebook provides another alternative implementation of Lab 03 that uses **LangChain's Bing Search tools** (`BingSearchResults` and `BingSearchAPIWrapper`) for external knowledge retrieval. This variant demonstrates the most modern approach using LangChain's standardized tool interfaces.

### Key Differences from Other Lab 03 Variants

#### Search Tool Implementation
- **Original:** Raw Tavily Search API with custom integration
- **Bing Websearch:** Direct Azure Bing Search SDK with custom wrapper
- **LangChain Bing (This variant):** LangChain's standardized `BingSearchResults` tool with `BingSearchAPIWrapper`

#### Architecture Advantages
- **Standardized Interface:** Uses LangChain's consistent tool interface across all search providers
- **Built-in Error Handling:** LangChain tools include robust error handling and retry logic
- **Tool Ecosystem Integration:** Seamless integration with other LangChain tools and agents
- **Simplified Implementation:** Pre-built tool abstractions reduce custom code requirements
- **Future-Proof:** Benefits from LangChain community improvements and updates

### Features Specific to LangChain Bing Search Variant
- **LangChain Tool Interface:** Native compatibility with LangChain's tool calling patterns
- **Simplified Tool Integration:** Uses `tool.invoke()` pattern consistent across LangChain ecosystem
- **Automatic Result Formatting:** Built-in result standardization for AI consumption
- **Enhanced Error Recovery:** LangChain's tool framework provides graceful error handling
- **Consistent API:** Same interface patterns as other LangChain search tools (Google, DuckDuckGo, etc.)

### Setup Requirements (LangChain Bing Search Variant)

#### Environment Configuration
```env
# Add to your .env file (note the variable name)
BING_SEARCH_API_KEY=your_bing_search_api_key_here
```

#### Azure Bing Search v7 Setup
1. **Create Bing Search Resource:**
   - Go to [Azure Portal](https://portal.azure.com/)
   - Create a new **Bing Search v7** resource
   - Copy the subscription key

2. **LangChain Tool Configuration:**
   ```python
   from langchain_community.tools.bing_search import BingSearchResults
   from langchain_community.utilities import BingSearchAPIWrapper
   
   # Initialize with proper API wrapper
   bing_search_wrapper = BingSearchAPIWrapper(
       bing_subscription_key=os.getenv("BING_SEARCH_API_KEY")
   )
   bing_tool = BingSearchResults(
       api_wrapper=bing_search_wrapper, 
       num_results=1
   )
   ```

### Tool Integration Implementation
```python
def execute_tools(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_ai_message = messages[-1]
    tool_messages = []
    
    if hasattr(last_ai_message, 'tool_calls') and last_ai_message.tool_calls:
        for tool_call in last_ai_message.tool_calls:
            if tool_call["name"] in ["AnswerQuestion", "ReviseAnswer"]:
                call_id = tool_call["id"]
                search_queries = tool_call["args"].get("search_queries", [])
                query_results = {}
                
                if bing_tool is not None:
                    for query in search_queries:
                        try:
                            # Uses LangChain's standardized tool interface
                            result = bing_tool.invoke(query)
                            query_results[query] = result
                        except Exception as e:
                            query_results[query] = f"Search error: {str(e)}"
                
                tool_message = ToolMessage(
                    content=json.dumps(query_results),
                    tool_call_id=call_id
                )
                tool_messages.append(tool_message)
    
    return {"messages": tool_messages}
```

### Error Handling and Graceful Degradation
The LangChain variant includes enhanced error handling:

```python
# Initialize Bing search tool with proper error handling
try:
    bing_search_wrapper = BingSearchAPIWrapper(
        bing_subscription_key=os.getenv("BING_SEARCH_API_KEY")
    )
    bing_tool = BingSearchResults(
        api_wrapper=bing_search_wrapper, 
        num_results=1
    )
    print("✅ Bing search tool initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing Bing search tool: {e}")
    print("Please set the BING_SEARCH_API_KEY environment variable")
    bing_tool = None
```

### Workflow Flow (Identical to Other Variants)
1. `START` → `Respond` (generate initial answer with search queries)
2. `Respond` → `Execute Tools` (perform Bing searches using LangChain tools)
3. `Execute Tools` → `Revisor` (synthesize research into improved response)
4. `Revisor` → `Execute Tools` (conditional: continue research if needed)
5. **Repeat steps 3-4** until research threshold is met (MAX_ITERATIONS = 4)
6. `Revisor` → `END` (finalize evidence-based response)

### Advantages of LangChain Bing Search Implementation
- **Ecosystem Integration:** Native compatibility with all LangChain tools and agents
- **Standardized Interface:** Consistent patterns across different search providers
- **Community Support:** Benefits from LangChain community improvements and bug fixes
- **Tool Chaining:** Easy integration with other LangChain tools in complex workflows
- **Simplified Maintenance:** Less custom code to maintain and debug
- **Flexible Switching:** Easy to swap between different search providers using same interface

### Required Python Packages
```bash
pip install langchain-community  # Includes BingSearchResults and BingSearchAPIWrapper
```

### When to Use the LangChain Bing Search Version
**Use this variant when:**
- You're building LangChain-based applications and want consistent tool interfaces
- You plan to use multiple LangChain tools in your workflow
- You prefer standardized, community-maintained tool implementations
- You want to easily switch between different search providers in the future
- You value ecosystem integration over custom implementations

### Comparison of All Lab 03 Variants

| Feature | Original (Tavily) | Bing Websearch | LangChain Bing |
|---------|------------------|----------------|----------------|
| **Search Provider** | Tavily API | Azure Bing Search SDK | LangChain Bing Tools |
| **Integration Type** | Direct API | Custom SDK wrapper | LangChain tool interface |
| **Code Complexity** | Medium | High (custom wrapper) | Low (standardized) |
| **Ecosystem Integration** | Tavily-specific | Azure-specific | LangChain ecosystem |
| **Maintenance** | API-dependent | Custom code maintenance | Community-maintained |
| **Flexibility** | Tavily features | Full Bing features | LangChain abstractions |
| **Error Handling** | Custom implementation | Custom implementation | Built-in LangChain handling |
| **Future-Proofing** | Tavily roadmap | Azure updates | LangChain community |

All three implementations provide identical AI agent capabilities with different external knowledge integration approaches, allowing you to choose based on your specific technical requirements, existing infrastructure, and development preferences.


## Prerequisites

- Python 3.11 or newer
- Jupyter Notebook or JupyterLab environment
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
    - `tavily-python` (for external knowledge retrieval in original Lab 03)
    - `azure-cognitiveservices-search-websearch` (for Bing Search integration in Lab 03 alternative)

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
     
     # Azure Bing Search API (required for Lab 03 Bing Search variants)
     BING_SEARCH_API_KEY=your_bing_search_api_key_here
     ```
4. Open and run the notebooks in the `src/notebooks/` directory.

### API Key Setup Guide

#### Azure OpenAI (Required for Labs 01.2, 02, 03)
1. Create an Azure OpenAI resource in the Azure Portal
2. Deploy a GPT model (recommended: `gpt-4o-mini`)
3. Copy the API key, endpoint, and API version from the Azure Portal

#### Tavily Search API (Required for Original Lab 03)
1. Sign up at [Tavily.com](https://tavily.com/)
2. Create a free account (includes generous free tier)
3. Generate an API key from your dashboard
4. Add the key to your `.env` file

#### Azure Bing Search API (Required for Lab 03 Bing Search Variants)
1. Go to [Azure Portal](https://portal.azure.com/)
2. Create a **Bing Search v7** resource
3. Choose your subscription and resource group
4. Select pricing tier (F1 free tier available for testing)
5. Copy the API key from the resource's "Keys and Endpoint" section
6. Add the key to your `.env` file as `BING_SEARCH_API_KEY`
7. The endpoint is typically: `https://api.bing.microsoft.com/`

**Note:** Both Bing Search variants (`lab03_02_reflexion_agent_using_bing_websearch.ipynb` and `lab03_03_reflexion_agent_using_langchain_tool_bing_search.ipynb`) use the same `BING_SEARCH_API_KEY` environment variable, making it easy to switch between implementations.

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
