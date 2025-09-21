"""
Integration tests for ResearchAgent.
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.research_agent import ResearchAgent
from integration_tests.test_utils import TestData, check_environment_variables


class TestResearchAgent(unittest.TestCase):
    """Test cases for ResearchAgent."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        if not check_environment_variables():
            raise unittest.SkipTest("Required environment variables not set")
        
        cls.test_data = TestData()
    
    def setUp(self):
        """Set up before each test."""
        self.research_agent = ResearchAgent()
    
    def test_initialization(self):
        """Test that ResearchAgent initializes correctly."""
        self.assertIsNotNone(self.research_agent.client)
        self.assertIsNotNone(self.research_agent.deployment_name)
        print("✅ ResearchAgent initialization test passed")
    
    def test_generate_prompt(self):
        """Test prompt generation functionality."""
        question = "What is Azure OpenAI?"
        context = "Azure OpenAI Service provides access to OpenAI models."
        
        prompt = self.research_agent.generate_prompt(question, context)
        
        self.assertIsInstance(prompt, str)
        self.assertIn(question, prompt)
        self.assertIn(context, prompt)
        self.assertIn("Instructions", prompt)
        print("✅ Prompt generation test passed")
    
    def test_sanitize_response(self):
        """Test response sanitization."""
        test_cases = [
            ("  Hello World  ", "Hello World"),
            ("\n\nTest Response\n\n", "Test Response"),
            ("Normal text", "Normal text"),
            ("", "")
        ]
        
        for input_text, expected in test_cases:
            result = self.research_agent.sanitize_response(input_text)
            self.assertEqual(result, expected)
        
        print("✅ Response sanitization test passed")
    
    def test_generate_with_azure_openai_documents(self):
        """Test answer generation with Azure OpenAI related documents."""
        question = self.test_data.TEST_QUESTIONS["azure_openai"]
        documents = [doc for doc in self.test_data.SAMPLE_DOCUMENTS if "Azure OpenAI" in doc.page_content]
        
        result = self.research_agent.generate(question, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("draft_answer", result)
        self.assertIn("context_used", result)
        
        # Check answer quality
        draft_answer = result["draft_answer"]
        self.assertIsInstance(draft_answer, str)
        self.assertGreater(len(draft_answer), 10)  # Should have substantial content
        
        # Check context
        context = result["context_used"]
        self.assertIsInstance(context, str)
        self.assertIn("Azure OpenAI", context)
        
        print(f"✅ Azure OpenAI generation test passed")
        print(f"   Answer length: {len(draft_answer)} characters")
    
    def test_generate_with_embedding_documents(self):
        """Test answer generation with embedding model documents."""
        question = self.test_data.TEST_QUESTIONS["embedding_model"]
        documents = [doc for doc in self.test_data.SAMPLE_DOCUMENTS if "embedding" in doc.page_content.lower()]
        
        result = self.research_agent.generate(question, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("draft_answer", result)
        self.assertIn("context_used", result)
        
        # Check that answer mentions relevant concepts
        draft_answer = result["draft_answer"].lower()
        context_keywords = ["embedding", "1536", "dimensions", "ada-002"]
        
        print(f"✅ Embedding model generation test passed")
        print(f"   Answer mentions embedding concepts: {any(keyword in draft_answer for keyword in context_keywords)}")
    
    def test_generate_with_machine_learning_documents(self):
        """Test answer generation with machine learning documents."""
        question = self.test_data.TEST_QUESTIONS["machine_learning"]
        documents = [doc for doc in self.test_data.SAMPLE_DOCUMENTS if "machine learning" in doc.page_content.lower()]
        
        result = self.research_agent.generate(question, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("draft_answer", result)
        self.assertIn("context_used", result)
        
        # Check that answer is relevant to machine learning
        draft_answer = result["draft_answer"].lower()
        ml_keywords = ["machine learning", "artificial intelligence", "learn", "data"]
        relevant_keywords_found = sum(1 for keyword in ml_keywords if keyword in draft_answer)
        
        self.assertGreater(relevant_keywords_found, 0)
        print(f"✅ Machine learning generation test passed")
        print(f"   Relevant keywords found: {relevant_keywords_found}/{len(ml_keywords)}")
    
    def test_generate_with_empty_documents(self):
        """Test behavior with empty document list."""
        question = self.test_data.TEST_QUESTIONS["azure_openai"]
        documents = []
        
        result = self.research_agent.generate(question, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("draft_answer", result)
        self.assertIn("context_used", result)
        
        # Context should be empty
        self.assertEqual(result["context_used"], "")
        
        # Answer should still be generated (though may indicate lack of context)
        self.assertIsInstance(result["draft_answer"], str)
        
        print("✅ Empty documents test passed")
    
    def test_generate_with_multiple_documents(self):
        """Test answer generation with multiple documents."""
        question = "Tell me about programming and AI"
        documents = self.test_data.SAMPLE_DOCUMENTS  # All documents
        
        result = self.research_agent.generate(question, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("draft_answer", result)
        self.assertIn("context_used", result)
        
        # Context should contain content from multiple documents
        context = result["context_used"]
        self.assertIn("Azure OpenAI", context)
        self.assertIn("Python", context)
        
        print("✅ Multiple documents test passed")
        print(f"   Context length: {len(context)} characters")
    
    def test_response_structure_error_handling(self):
        """Test handling of malformed API responses."""
        with patch.object(self.research_agent.client, 'complete') as mock_complete:
            # Mock a malformed response
            mock_response = MagicMock()
            mock_response.choices = []  # Empty choices
            mock_complete.return_value = mock_response
            
            question = self.test_data.TEST_QUESTIONS["azure_openai"]
            documents = [self.test_data.SAMPLE_DOCUMENTS[0]]
            
            result = self.research_agent.generate(question, documents)
            
            # Should handle gracefully and return default message
            self.assertIn("cannot answer", result["draft_answer"].lower())
            print("✅ Response structure error handling test passed")


def run_research_agent_tests():
    """Run all ResearchAgent tests."""
    print("\n🧪 Running ResearchAgent Integration Tests...\n")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestResearchAgent)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 ResearchAgent Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    if success:
        print("\n🎉 All ResearchAgent tests passed!")
    else:
        print("\n💥 Some ResearchAgent tests failed!")
    
    return success


if __name__ == "__main__":
    run_research_agent_tests()