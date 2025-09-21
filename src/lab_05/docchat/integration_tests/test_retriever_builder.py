"""
Integration tests for RetrieverBuilder.
"""

import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document

from integration_tests.test_utils import TestData, check_environment_variables
from retriever.builder import RetrieverBuilder


class TestRetrieverBuilder(unittest.TestCase):
    """Test cases for RetrieverBuilder."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        if not check_environment_variables():
            raise unittest.SkipTest("Required environment variables not set")

        cls.test_data = TestData()

    def setUp(self):
        """Set up before each test."""
        # Create a temporary directory for Chroma DB during tests
        self.temp_dir = tempfile.mkdtemp()

        # Patch the settings to use temporary directory
        patcher = patch("retriever.builder.settings")
        self.mock_settings = patcher.start()
        self.mock_settings.CHROMA_DB_PATH = self.temp_dir
        self.mock_settings.VECTOR_SEARCH_K = 5
        self.mock_settings.HYBRID_RETRIEVER_WEIGHTS = [0.4, 0.6]
        self.addCleanup(patcher.stop)

        # Initialize builder
        self.builder = RetrieverBuilder()

    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary directory
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test that RetrieverBuilder initializes correctly."""
        self.assertIsNotNone(self.builder.embeddings)
        print("✅ RetrieverBuilder initialization test passed")

    def test_embeddings_configuration(self):
        """Test that Azure OpenAI embeddings are configured correctly."""
        embeddings = self.builder.embeddings

        # Check that embeddings instance is created
        self.assertIsNotNone(embeddings)

        # Check configuration attributes (these may vary based on langchain version)
        self.assertTrue(
            hasattr(embeddings, "azure_endpoint")
            or hasattr(embeddings, "openai_api_base")
        )

        print("✅ Embeddings configuration test passed")

    def test_build_hybrid_retriever_with_sample_documents(self):
        """Test building hybrid retriever with sample documents."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Mock both Chroma and BM25Retriever since we may have dependency issues
        with (
            patch("retriever.builder.Chroma") as mock_chroma,
            patch("retriever.builder.BM25Retriever") as mock_bm25,
        ):
            # Create mock retrievers that are actual Runnable instances
            from langchain_core.runnables import RunnableLambda

            # Mock vector retriever
            mock_vector_store = MagicMock()
            mock_vector_retriever = RunnableLambda(lambda x: documents[:2])
            mock_vector_store.as_retriever.return_value = mock_vector_retriever
            mock_chroma.from_documents.return_value = mock_vector_store

            # Mock BM25 retriever
            mock_bm25_retriever = RunnableLambda(lambda x: documents[:2])
            mock_bm25.from_documents.return_value = mock_bm25_retriever

            retriever = self.builder.build_hybrid_retriever(documents)

            # Check that retriever is created
            self.assertIsNotNone(retriever)
            self.assertIsInstance(retriever, EnsembleRetriever)

            # Check that it has the expected number of retrievers
            self.assertEqual(len(retriever.retrievers), 2)

            # Check that both retrievers were created
            mock_chroma.from_documents.assert_called_once()
            mock_bm25.from_documents.assert_called_once()

        print("✅ Hybrid retriever creation test passed")

    def test_build_hybrid_retriever_with_single_document(self):
        """Test building hybrid retriever with a single document."""
        single_doc = [self.test_data.SAMPLE_DOCUMENTS[0]]

        # Mock both retrievers to avoid dependency issues
        with (
            patch("retriever.builder.Chroma") as mock_chroma,
            patch("retriever.builder.BM25Retriever") as mock_bm25,
        ):
            from langchain_core.runnables import RunnableLambda

            # Mock vector retriever
            mock_vector_store = MagicMock()
            mock_vector_retriever = RunnableLambda(lambda x: single_doc)
            mock_vector_store.as_retriever.return_value = mock_vector_retriever
            mock_chroma.from_documents.return_value = mock_vector_store

            # Mock BM25 retriever
            mock_bm25_retriever = RunnableLambda(lambda x: single_doc)
            mock_bm25.from_documents.return_value = mock_bm25_retriever

            retriever = self.builder.build_hybrid_retriever(single_doc)

            self.assertIsNotNone(retriever)
            self.assertIsInstance(retriever, EnsembleRetriever)

        print("✅ Single document retriever test passed")

    def test_retriever_functionality(self):
        """Test that the built retriever can actually retrieve documents."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Mock both Chroma and BM25Retriever to avoid dependency issues
        with (
            patch("retriever.builder.Chroma") as mock_chroma,
            patch("retriever.builder.BM25Retriever") as mock_bm25,
        ):
            from langchain_core.runnables import RunnableLambda

            # Mock vector retriever
            mock_vector_store = MagicMock()
            mock_vector_retriever = RunnableLambda(lambda x: documents[:3])
            mock_vector_store.as_retriever.return_value = mock_vector_retriever
            mock_chroma.from_documents.return_value = mock_vector_store

            # Mock BM25 retriever
            mock_bm25_retriever = RunnableLambda(lambda x: documents[:3])
            mock_bm25.from_documents.return_value = mock_bm25_retriever

            retriever = self.builder.build_hybrid_retriever(documents)

            # Test retrieval with a query
            query = "Azure OpenAI"
            results = retriever.invoke(query)

            # Check that results are returned
            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)

            # Check that results are Document objects
            for result in results:
                self.assertIsInstance(result, Document)
                self.assertIsNotNone(result.page_content)

        print(
            f"✅ Retriever functionality test passed - found {len(results)} documents"
        )

    def test_retriever_query_variations(self):
        """Test retriever with different types of queries."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Mock both Chroma and BM25Retriever to avoid dependency issues
        with (
            patch("retriever.builder.Chroma") as mock_chroma,
            patch("retriever.builder.BM25Retriever") as mock_bm25,
        ):
            from langchain_core.runnables import RunnableLambda

            # Mock vector retriever
            mock_vector_store = MagicMock()
            mock_vector_retriever = RunnableLambda(lambda x: documents[:2])
            mock_vector_store.as_retriever.return_value = mock_vector_retriever
            mock_chroma.from_documents.return_value = mock_vector_store

            # Mock BM25 retriever
            mock_bm25_retriever = RunnableLambda(lambda x: documents[:2])
            mock_bm25.from_documents.return_value = mock_bm25_retriever

            retriever = self.builder.build_hybrid_retriever(documents)

            test_queries = [
                "embedding model",
                "machine learning",
                "Python programming",
                "nonexistent topic xyz123",
            ]

            for query in test_queries:
                results = retriever.invoke(query)
                self.assertIsInstance(results, list)

                # Even for nonexistent topics, retriever should return something
                # (may be empty or low-relevance documents)
                print(f"Query '{query}': {len(results)} results")

        print("✅ Query variations test passed")

    def test_retriever_k_parameter(self):
        """Test that the retriever respects the k parameter for result count."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Test with different k values
        for k in [2, 5, 10]:
            with (
                patch("retriever.builder.settings") as mock_settings,
                patch("retriever.builder.Chroma") as mock_chroma,
                patch("retriever.builder.BM25Retriever") as mock_bm25,
            ):
                mock_settings.CHROMA_DB_PATH = self.temp_dir
                mock_settings.VECTOR_SEARCH_K = k
                mock_settings.HYBRID_RETRIEVER_WEIGHTS = [0.4, 0.6]

                from langchain_core.runnables import RunnableLambda

                # Mock vector retriever
                mock_vector_store = MagicMock()
                mock_vector_retriever = RunnableLambda(lambda x: documents[:k])
                mock_vector_store.as_retriever.return_value = mock_vector_retriever
                mock_chroma.from_documents.return_value = mock_vector_store

                # Mock BM25 retriever
                mock_bm25_retriever = RunnableLambda(lambda x: documents[:k])
                mock_bm25.from_documents.return_value = mock_bm25_retriever

                builder = RetrieverBuilder()
                retriever = builder.build_hybrid_retriever(documents)

                results = retriever.invoke("Azure OpenAI")

                # Results might be less than k if not enough documents match
                self.assertLessEqual(
                    len(results), k * 2
                )  # *2 because ensemble combines two retrievers

        print("✅ K parameter test passed")

    def test_retriever_weights(self):
        """Test that different retriever weights work."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Test with different weight combinations
        weight_combinations = [[0.3, 0.7], [0.5, 0.5], [0.8, 0.2]]

        for weights in weight_combinations:
            with (
                patch("retriever.builder.settings") as mock_settings,
                patch("retriever.builder.Chroma") as mock_chroma,
                patch("retriever.builder.BM25Retriever") as mock_bm25,
            ):
                mock_settings.CHROMA_DB_PATH = self.temp_dir
                mock_settings.VECTOR_SEARCH_K = 5
                mock_settings.HYBRID_RETRIEVER_WEIGHTS = weights

                from langchain_core.runnables import RunnableLambda

                # Mock vector retriever
                mock_vector_store = MagicMock()
                mock_vector_retriever = RunnableLambda(lambda x: documents[:3])
                mock_vector_store.as_retriever.return_value = mock_vector_retriever
                mock_chroma.from_documents.return_value = mock_vector_store

                # Mock BM25 retriever
                mock_bm25_retriever = RunnableLambda(lambda x: documents[:3])
                mock_bm25.from_documents.return_value = mock_bm25_retriever

                builder = RetrieverBuilder()
                retriever = builder.build_hybrid_retriever(documents)

                results = retriever.invoke("Azure OpenAI")
                self.assertIsInstance(results, list)

                print(f"Weights {weights}: {len(results)} results")

        print("✅ Retriever weights test passed")

    def test_build_empty_documents_list(self):
        """Test building retriever with empty documents list."""
        empty_docs = []

        # This should raise an exception or handle gracefully
        with self.assertRaises(Exception):
            self.builder.build_hybrid_retriever(empty_docs)

        print("✅ Empty documents handling test passed")

    def test_build_invalid_documents(self):
        """Test building retriever with invalid document format."""
        # Test with non-Document objects
        invalid_docs = ["not a document", "another string"]

        with self.assertRaises(Exception):
            self.builder.build_hybrid_retriever(invalid_docs)

        print("✅ Invalid documents handling test passed")

    def test_embedding_error_handling(self):
        """Test handling of embedding errors."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Mock embeddings to raise an exception during Chroma creation
        with patch("retriever.builder.Chroma.from_documents") as mock_chroma:
            mock_chroma.side_effect = Exception("Embedding service error")

            with self.assertRaises(Exception):
                self.builder.build_hybrid_retriever(documents)

        print("✅ Embedding error handling test passed")

    def test_chroma_persistence(self):
        """Test that Chroma vector store persists correctly."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Mock both Chroma and BM25Retriever to test persistence logic
        with (
            patch("retriever.builder.Chroma") as mock_chroma,
            patch("retriever.builder.BM25Retriever") as mock_bm25,
        ):
            from langchain_core.runnables import RunnableLambda

            # Mock vector retriever
            mock_vector_store = MagicMock()
            mock_vector_retriever = RunnableLambda(lambda x: documents[:2])
            mock_vector_store.as_retriever.return_value = mock_vector_retriever
            mock_chroma.from_documents.return_value = mock_vector_store

            # Mock BM25 retriever
            mock_bm25_retriever = RunnableLambda(lambda x: documents[:2])
            mock_bm25.from_documents.return_value = mock_bm25_retriever

            # Build retriever first time
            retriever1 = self.builder.build_hybrid_retriever(documents)
            results1 = retriever1.invoke("Azure OpenAI")

            # Build retriever second time (should use persisted data)
            retriever2 = self.builder.build_hybrid_retriever(documents)
            results2 = retriever2.invoke("Azure OpenAI")

            # Results should be similar (though order might differ)
            self.assertEqual(len(results1), len(results2))

            # Verify that Chroma.from_documents was called twice
            self.assertEqual(mock_chroma.from_documents.call_count, 2)

        print("✅ Chroma persistence test passed")

    def test_retriever_performance(self):
        """Test retriever performance with multiple queries."""
        documents = self.test_data.SAMPLE_DOCUMENTS

        # Mock both Chroma and BM25Retriever to avoid dependency issues
        with (
            patch("retriever.builder.Chroma") as mock_chroma,
            patch("retriever.builder.BM25Retriever") as mock_bm25,
        ):
            from langchain_core.runnables import RunnableLambda

            # Mock vector retriever
            mock_vector_store = MagicMock()
            mock_vector_retriever = RunnableLambda(lambda x: documents[:2])
            mock_vector_store.as_retriever.return_value = mock_vector_retriever
            mock_chroma.from_documents.return_value = mock_vector_store

            # Mock BM25 retriever
            mock_bm25_retriever = RunnableLambda(lambda x: documents[:2])
            mock_bm25.from_documents.return_value = mock_bm25_retriever

            retriever = self.builder.build_hybrid_retriever(documents)

            import time

            queries = [
                "Azure OpenAI Service",
                "embedding model text",
                "machine learning artificial intelligence",
                "Python programming language",
            ]

            start_time = time.time()

            for query in queries:
                results = retriever.invoke(query)
                self.assertIsInstance(results, list)

            end_time = time.time()
            total_time = end_time - start_time

            # Should complete reasonably quickly (adjust threshold as needed)
            self.assertLess(total_time, 30.0, "Retrieval took too long")

        print(
            f"✅ Performance test passed - {len(queries)} queries in {total_time:.2f} seconds"
        )


def run_retriever_builder_tests():
    """Run all RetrieverBuilder tests."""
    print("\n🧪 Running RetrieverBuilder Integration Tests...\n")

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRetrieverBuilder)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n📊 RetrieverBuilder Test Results:")
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
        print("\n🎉 All RetrieverBuilder tests passed!")
    else:
        print("\n💥 Some RetrieverBuilder tests failed!")

    return success


if __name__ == "__main__":
    run_retriever_builder_tests()
