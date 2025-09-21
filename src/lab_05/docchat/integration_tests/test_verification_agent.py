"""
Integration tests for VerificationAgent.
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.verification_agent import VerificationAgent
from integration_tests.test_utils import TestData, check_environment_variables


class TestVerificationAgent(unittest.TestCase):
    """Test cases for VerificationAgent."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        if not check_environment_variables():
            raise unittest.SkipTest("Required environment variables not set")
        
        cls.test_data = TestData()
    
    def setUp(self):
        """Set up before each test."""
        self.verification_agent = VerificationAgent()
    
    def test_initialization(self):
        """Test that VerificationAgent initializes correctly."""
        self.assertIsNotNone(self.verification_agent.client)
        self.assertIsNotNone(self.verification_agent.deployment_name)
        print("✅ VerificationAgent initialization test passed")
    
    def test_generate_prompt(self):
        """Test prompt generation functionality."""
        answer = "Azure OpenAI provides access to language models."
        context = "Azure OpenAI Service provides REST API access to OpenAI's powerful language models."
        
        prompt = self.verification_agent.generate_prompt(answer, context)
        
        self.assertIsInstance(prompt, str)
        self.assertIn(answer, prompt)
        self.assertIn(context, prompt)
        self.assertIn("Supported:", prompt)
        self.assertIn("Contradictions:", prompt)
        print("✅ Prompt generation test passed")
    
    def test_sanitize_response(self):
        """Test response sanitization."""
        test_cases = [
            ("  Verification report  ", "Verification report"),
            ("\n\nSupported: YES\n\n", "Supported: YES"),
            ("Normal text", "Normal text"),
            ("", "")
        ]
        
        for input_text, expected in test_cases:
            result = self.verification_agent.sanitize_response(input_text)
            self.assertEqual(result, expected)
        
        print("✅ Response sanitization test passed")
    
    def test_parse_verification_response(self):
        """Test parsing of LLM verification responses."""
        # Test valid response
        valid_response = """
        Supported: YES
        Unsupported Claims: []
        Contradictions: []
        Relevant: YES
        Additional Details: The answer is well supported by the context.
        """
        
        result = self.verification_agent.parse_verification_response(valid_response)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Supported"], "YES")
        self.assertEqual(result["Unsupported Claims"], [])
        self.assertEqual(result["Contradictions"], [])
        self.assertEqual(result["Relevant"], "YES")
        self.assertIn("supported", result["Additional Details"])
        
        print("✅ Valid response parsing test passed")
    
    def test_parse_verification_response_with_claims(self):
        """Test parsing responses with unsupported claims and contradictions."""
        response_with_claims = """
        Supported: PARTIAL
        Unsupported Claims: [claim1, claim2]
        Contradictions: [contradiction1]
        Relevant: YES
        Additional Details: Some claims are not supported.
        """
        
        result = self.verification_agent.parse_verification_response(response_with_claims)
        
        self.assertEqual(result["Supported"], "PARTIAL")
        self.assertEqual(result["Unsupported Claims"], ["claim1", "claim2"])
        self.assertEqual(result["Contradictions"], ["contradiction1"])
        
        print("✅ Claims parsing test passed")
    
    def test_parse_verification_response_malformed(self):
        """Test parsing of malformed responses."""
        malformed_response = "This is not a valid verification response format."
        
        result = self.verification_agent.parse_verification_response(malformed_response)
        
        self.assertIsNone(result)
        print("✅ Malformed response parsing test passed")
    
    def test_format_verification_report(self):
        """Test formatting of verification reports."""
        verification = {
            "Supported": "YES",
            "Unsupported Claims": ["claim1", "claim2"],
            "Contradictions": [],
            "Relevant": "YES",
            "Additional Details": "Test details"
        }
        
        report = self.verification_agent.format_verification_report(verification)
        
        self.assertIsInstance(report, str)
        self.assertIn("**Supported:** YES", report)
        self.assertIn("**Unsupported Claims:** claim1, claim2", report)
        self.assertIn("**Contradictions:** None", report)
        self.assertIn("**Additional Details:** Test details", report)
        
        print("✅ Report formatting test passed")
    
    def test_check_supported_answer(self):
        """Test verification of a well-supported answer."""
        answer = self.test_data.EXPECTED_ANSWERS["azure_openai"]
        documents = [doc for doc in self.test_data.SAMPLE_DOCUMENTS if "Azure OpenAI" in doc.page_content]
        
        result = self.verification_agent.check(answer, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("verification_report", result)
        self.assertIn("context_used", result)
        
        # Check report content
        report = result["verification_report"]
        self.assertIsInstance(report, str)
        self.assertIn("**Supported:**", report)
        self.assertIn("**Relevant:**", report)
        
        # Check context
        context = result["context_used"]
        self.assertIn("Azure OpenAI", context)
        
        print(f"✅ Supported answer verification test passed")
    
    def test_check_embedding_answer(self):
        """Test verification of embedding model answer."""
        answer = self.test_data.EXPECTED_ANSWERS["embedding_model"]
        documents = [doc for doc in self.test_data.SAMPLE_DOCUMENTS if "embedding" in doc.page_content.lower()]
        
        result = self.verification_agent.check(answer, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("verification_report", result)
        self.assertIn("context_used", result)
        
        report = result["verification_report"]
        context = result["context_used"]
        
        # Should find relevant information about embeddings
        self.assertIn("embedding", context.lower())
        
        print(f"✅ Embedding answer verification test passed")
    
    def test_check_unsupported_answer(self):
        """Test verification of an unsupported answer."""
        # Answer about weather with tech documents
        unsupported_answer = "The weather today is sunny and 75 degrees."
        documents = self.test_data.SAMPLE_DOCUMENTS
        
        result = self.verification_agent.check(unsupported_answer, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("verification_report", result)
        self.assertIn("context_used", result)
        
        report = result["verification_report"]
        
        # The answer should not be well supported by tech documents
        print(f"✅ Unsupported answer verification test passed")
    
    def test_check_contradictory_answer(self):
        """Test verification of a contradictory answer."""
        # Answer that contradicts the documents
        contradictory_answer = "Azure OpenAI Service is not available for public use and doesn't provide API access."
        documents = [doc for doc in self.test_data.SAMPLE_DOCUMENTS if "Azure OpenAI" in doc.page_content]
        
        result = self.verification_agent.check(contradictory_answer, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("verification_report", result)
        
        print(f"✅ Contradictory answer verification test passed")
    
    def test_check_empty_documents(self):
        """Test verification with empty document list."""
        answer = self.test_data.EXPECTED_ANSWERS["azure_openai"]
        documents = []
        
        result = self.verification_agent.check(answer, documents)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertIn("verification_report", result)
        self.assertIn("context_used", result)
        
        # Context should be empty
        self.assertEqual(result["context_used"], "")
        
        print("✅ Empty documents verification test passed")
    
    
    def test_response_structure_error_handling(self):
        """Test handling of malformed API responses."""
        with patch.object(self.verification_agent.client, 'complete') as mock_complete:
            # Mock a malformed response structure
            mock_response = MagicMock()
            mock_response.choices = []  # Empty choices
            mock_complete.return_value = mock_response
            
            answer = self.test_data.EXPECTED_ANSWERS["azure_openai"]
            documents = [self.test_data.SAMPLE_DOCUMENTS[0]]
            
            result = self.verification_agent.check(answer, documents)
            
            # Should handle gracefully and return default verification
            self.assertIn("Invalid response structure", result["verification_report"])
            print("✅ Response structure error handling test passed")
    
    def test_empty_llm_response(self):
        """Test handling of empty LLM responses."""
        with patch.object(self.verification_agent.client, 'complete') as mock_complete:
            # Mock an empty response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = ""
            mock_complete.return_value = mock_response
            
            answer = self.test_data.EXPECTED_ANSWERS["azure_openai"]
            documents = [self.test_data.SAMPLE_DOCUMENTS[0]]
            
            result = self.verification_agent.check(answer, documents)
            
            # Should handle empty response gracefully
            self.assertIn("Empty response", result["verification_report"])
            print("✅ Empty LLM response handling test passed")


def run_verification_agent_tests():
    """Run all VerificationAgent tests."""
    print("\n🧪 Running VerificationAgent Integration Tests...\n")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVerificationAgent)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 VerificationAgent Test Results:")
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
        print("\n🎉 All VerificationAgent tests passed!")
    else:
        print("\n💥 Some VerificationAgent tests failed!")
    
    return success


if __name__ == "__main__":
    run_verification_agent_tests()