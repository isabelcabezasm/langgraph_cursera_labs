# Agent Integration Tests

This directory contains comprehensive integration tests for all agents and components in the docchat application:

- **RelevanceChecker**: Tests document relevance classification
- **ResearchAgent**: Tests answer generation from documents  
- **VerificationAgent**: Tests answer verification against source documents
- **RetrieverBuilder**: Tests hybrid retrieval system (BM25 + vector embeddings)

## Prerequisites

1. **Environment Variables**: Ensure these are set in your `.env` file:
   ```
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment
   AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT=your_embedding_deployment
   OPENAI_API_VERSION=your_api_version
   ```

2. **Dependencies**: Install required packages:
   ```bash
   pip install azure-ai-inference azure-core langchain-openai python-dotenv
   ```

## Running Tests

### Run All Tests
```bash
cd /workspaces/cursera_labs/src/lab_05/docchat
python tests/run_tests.py
```

### Run Specific Agent Tests
```bash
# RelevanceChecker only
python tests/run_tests.py relevance

# ResearchAgent only  
python tests/run_tests.py research

# VerificationAgent only
python tests/run_tests.py verification

# RetrieverBuilder only
python tests/run_tests.py builder
```

### Run Individual Test Files
```bash
# Individual test files
python tests/test_relevance_checker.py
python tests/test_research_agent.py
python tests/test_verification_agent.py
python tests/test_retriever_builder.py
```

## Test Coverage

### RelevanceChecker Tests
- ✅ Agent initialization
- ✅ CAN_ANSWER classification
- ✅ PARTIAL classification  
- ✅ NO_MATCH classification
- ✅ Empty retriever handling
- ✅ Different k values
- ✅ Error handling
- ✅ Response validation

### ResearchAgent Tests
- ✅ Agent initialization
- ✅ Prompt generation
- ✅ Response sanitization
- ✅ Answer generation with various document types
- ✅ Empty documents handling
- ✅ Multiple documents processing
- ✅ Error handling
- ✅ Malformed response handling

### VerificationAgent Tests
- ✅ Agent initialization
- ✅ Prompt generation
- ✅ Response sanitization
- ✅ Verification response parsing
- ✅ Report formatting
- ✅ Supported answer verification
- ✅ Unsupported answer detection
- ✅ Contradictory answer detection
- ✅ Empty documents handling
- ✅ Error handling
- ✅ Malformed response handling

### RetrieverBuilder Tests
- ✅ Builder initialization
- ✅ Azure OpenAI embeddings configuration
- ✅ Hybrid retriever creation (BM25 + vector)
- ✅ Single and multiple document handling
- ✅ Retrieval functionality testing
- ✅ Query variation handling
- ✅ K parameter configuration
- ✅ Retriever weight configuration
- ✅ Empty documents error handling
- ✅ Invalid documents error handling
- ✅ Embedding error handling
- ✅ Chroma persistence testing
- ✅ Performance testing

## Test Data

The tests use realistic sample documents covering:
- Azure OpenAI Service documentation
- Text embedding model information
- Machine learning concepts
- Python programming language

This ensures comprehensive testing across different domains and content types.

## Expected Output

When all tests pass, you should see:
```
🎉 ALL AGENT TESTS PASSED! 🎉
Your Azure OpenAI agent integration is working correctly!
```

If tests fail, detailed error information will be provided to help debug issues.

## Troubleshooting

1. **Import Errors**: Ensure you're running from the correct directory and all dependencies are installed
2. **API Errors**: Verify your Azure OpenAI credentials and endpoint are correct
3. **Rate Limiting**: Azure OpenAI may rate limit requests; re-run tests if needed
4. **Network Issues**: Ensure you have internet connectivity to reach Azure OpenAI services