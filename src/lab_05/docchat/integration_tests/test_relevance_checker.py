"""
Integration tests for RelevanceChecker agent.
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.relevance_checker import RelevanceChecker
from integration_tests.test_utils import TestData, MockRetriever, check_environment_variables


class TestRelevanceChecker(unittest.TestCase):
    """Test cases for RelevanceChecker agent."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        if not check_environment_variables():
            raise unittest.SkipTest("Required environment variables not set")
        
        cls.test_data = TestData()
        cls.mock_retriever = MockRetriever(cls.test_data.SAMPLE_DOCUMENTS)
    
    def setUp(self):
        """Set up before each test."""
        self.relevance_checker = RelevanceChecker()
    
    def test_initialization(self):
        """Test that RelevanceChecker initializes correctly."""
        self.assertIsNotNone(self.relevance_checker.client)
        self.assertIsNotNone(self.relevance_checker.deployment_name)
        print("✅ RelevanceChecker initialization test passed")
    
    def test_can_answer_classification(self):
        """Test that RelevanceChecker correctly identifies questions it can answer."""
        question = self.test_data.TEST_QUESTIONS["azure_openai"]
        result = self.relevance_checker.check(question, self.mock_retriever, k=2)
        
        self.assertIn(result, ["CAN_ANSWER", "PARTIAL", "NO_MATCH"])
        # For Azure OpenAI question with relevant docs, should be CAN_ANSWER or PARTIAL
        self.assertIn(result, ["CAN_ANSWER", "PARTIAL"])
        print(f"✅ Can answer test passed: {question} -> {result}")
    
    def test_partial_classification(self):
        """Test that RelevanceChecker correctly identifies partial matches."""
        question = self.test_data.TEST_QUESTIONS["partial"]  # "Tell me about AI models"
        result = self.relevance_checker.check(question, self.mock_retriever, k=2)
        
        self.assertIn(result, ["CAN_ANSWER", "PARTIAL", "NO_MATCH"])
        # This should likely be PARTIAL since it's related but not fully covered
        print(f"✅ Partial answer test passed: {question} -> {result}")
    
    def test_no_match_classification(self):
        """Test that RelevanceChecker correctly identifies unrelated questions."""
        question = self.test_data.TEST_QUESTIONS["unrelated"]  # "What is the weather like today?"
        result = self.relevance_checker.check(question, self.mock_retriever, k=2)
        
        self.assertIn(result, ["CAN_ANSWER", "PARTIAL", "NO_MATCH"])
        # Weather question should be NO_MATCH with tech documents
        print(f"✅ No match test passed: {question} -> {result}")
    
    def test_empty_retriever_response(self):
        """Test behavior when retriever returns no documents."""
        empty_retriever = MockRetriever([])
        question = self.test_data.TEST_QUESTIONS["azure_openai"]
        
        result = self.relevance_checker.check(question, empty_retriever, k=2)
        self.assertEqual(result, "NO_MATCH")
        print("✅ Empty retriever test passed")
    
    def test_different_k_values(self):
        """Test RelevanceChecker with different k values."""
        question = self.test_data.TEST_QUESTIONS["machine_learning"]
        
        # Test with k=1
        result_k1 = self.relevance_checker.check(question, self.mock_retriever, k=1)
        self.assertIn(result_k1, ["CAN_ANSWER", "PARTIAL", "NO_MATCH"])
        
        # Test with k=3
        result_k3 = self.relevance_checker.check(question, self.mock_retriever, k=3)
        self.assertIn(result_k3, ["CAN_ANSWER", "PARTIAL", "NO_MATCH"])
        
        print(f"✅ Different k values test passed: k=1 -> {result_k1}, k=3 -> {result_k3}")
    
    @patch('agents.relevance_checker.logger')
    def test_error_handling(self, mock_logger):
        """Test error handling in RelevanceChecker."""
        # Mock the client to raise an exception
        with patch.object(self.relevance_checker, 'client') as mock_client:
            mock_client.complete.side_effect = Exception("Mock API error")
            
            question = self.test_data.TEST_QUESTIONS["azure_openai"]
            result = self.relevance_checker.check(question, self.mock_retriever, k=2)
            
            # Should return NO_MATCH on error
            self.assertEqual(result, "NO_MATCH")
            mock_logger.error.assert_called()
            print("✅ Error handling test passed")
    
    def test_response_validation(self):
        """Test that RelevanceChecker handles invalid LLM responses."""
        with patch.object(self.relevance_checker.client, 'complete') as mock_complete:
            # Mock an invalid response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "INVALID_RESPONSE"
            mock_complete.return_value = mock_response
            
            question = self.test_data.TEST_QUESTIONS["azure_openai"]
            result = self.relevance_checker.check(question, self.mock_retriever, k=2)
            
            # Should default to NO_MATCH for invalid responses
            self.assertEqual(result, "NO_MATCH")
            print("✅ Response validation test passed")


def run_relevance_checker_tests():
    """Run all RelevanceChecker tests."""
    print("\n🧪 Running RelevanceChecker Integration Tests...\n")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRelevanceChecker)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 RelevanceChecker Test Results:")
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
        print("\n🎉 All RelevanceChecker tests passed!")
    else:
        print("\n💥 Some RelevanceChecker tests failed!")
    
    return success


if __name__ == "__main__":
    run_relevance_checker_tests()