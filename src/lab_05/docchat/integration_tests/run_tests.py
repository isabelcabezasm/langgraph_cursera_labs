#!/usr/bin/env python3
"""
Comprehensive test runner for all agent integration tests.
"""

import importlib.util
import os
import sys
import time
from datetime import datetime

from integration_tests.test_relevance_checker import run_relevance_checker_tests
from integration_tests.test_research_agent import run_research_agent_tests
from integration_tests.test_retriever_builder import run_retriever_builder_tests
from integration_tests.test_utils import check_environment_variables
from integration_tests.test_verification_agent import run_verification_agent_tests


def print_banner():
    """Print a nice banner for the test suite."""
    print("=" * 80)
    print("🤖 AGENT INTEGRATION TEST SUITE")
    print("=" * 80)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📂 Working directory: {os.getcwd()}")
    print("=" * 80)


def check_prerequisites():
    """Check if all prerequisites are met before running tests."""
    print("🔍 Checking prerequisites...")

    # Check environment variables
    if not check_environment_variables():
        print("❌ Environment variables check failed!")
        return False

    print("✅ Environment variables check passed!")
    # Check if required modules can be imported (without importing unused symbols)
    try:
        modules = [
            "agents.relevance_checker",
            "agents.research_agent",
            "agents.verification_agent",
            "retriever.builder",
        ]

        missing = [m for m in modules if importlib.util.find_spec(m) is None]
        if missing:
            print(f"❌ Missing required modules: {', '.join(missing)}")
            return False

        print("✅ Agent modules and retriever import check passed!")
    except Exception as e:
        print(f"❌ Failed to verify agent modules or retriever: {e}")
        return False
        return False

    # Check if Azure AI packages are available
    try:
        missing = [
            m
            for m in ("azure.ai.inference", "azure.core.credentials")
            if importlib.util.find_spec(m) is None
        ]
        if missing:
            print(f"❌ Azure AI packages not available: {', '.join(missing)}")
            return False

        print("✅ Azure AI packages check passed!")
    except Exception as e:
        print(f"❌ Azure AI package check failed: {e}")
        return False

    print("🎉 All prerequisites met!")
    return True


def run_all_tests():
    """Run all agent integration tests."""
    print_banner()

    # Check prerequisites
    if not check_prerequisites():
        print("\n💥 Prerequisites not met. Exiting...")
        return False

    print("\n🚀 Starting agent integration tests...\n")

    start_time = time.time()
    test_results = {}

    # Run RelevanceChecker tests
    print("1️⃣ " + "=" * 60)
    try:
        test_results["relevance_checker"] = run_relevance_checker_tests()
    except Exception as e:
        print(f"💥 RelevanceChecker tests failed with exception: {e}")
        test_results["relevance_checker"] = False

    print("\n")

    # Run ResearchAgent tests
    print("2️⃣ " + "=" * 60)
    try:
        test_results["research_agent"] = run_research_agent_tests()
    except Exception as e:
        print(f"💥 ResearchAgent tests failed with exception: {e}")
        test_results["research_agent"] = False

    print("\n")

    # Run VerificationAgent tests
    print("3️⃣ " + "=" * 60)
    try:
        test_results["verification_agent"] = run_verification_agent_tests()
    except Exception as e:
        print(f"💥 VerificationAgent tests failed with exception: {e}")
        test_results["verification_agent"] = False

    print("\n")

    # Run RetrieverBuilder tests
    print("4️⃣ " + "=" * 60)
    try:
        test_results["retriever_builder"] = run_retriever_builder_tests()
    except Exception as e:
        print(f"💥 RetrieverBuilder tests failed with exception: {e}")
        test_results["retriever_builder"] = False

    # Calculate total time
    end_time = time.time()
    total_time = end_time - start_time

    # Print final summary
    print("\n" + "=" * 80)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 80)

    passed_count = sum(1 for result in test_results.values() if result)
    total_count = len(test_results)

    print(f"🧪 Test Suites Run: {total_count}")
    print(f"✅ Test Suites Passed: {passed_count}")
    print(f"❌ Test Suites Failed: {total_count - passed_count}")
    print(f"⏱️  Total Time: {total_time:.2f} seconds")

    print("\nDetailed Results:")
    for agent, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {agent.replace('_', ' ').title()}: {status}")

    all_passed = all(test_results.values())

    if all_passed:
        print("\n🎉 ALL AGENT TESTS PASSED! 🎉")
        print("Your Azure OpenAI agent integration is working correctly!")
    else:
        print("\n💥 SOME TESTS FAILED!")
        print("Please check the detailed output above for specific failures.")

    print("=" * 80)
    return all_passed


def run_specific_agent_test(agent_name):
    """Run tests for a specific agent."""
    agent_name = agent_name.lower().replace("-", "_").replace(" ", "_")

    if agent_name in ["relevance", "relevance_checker"]:
        print("Running RelevanceChecker tests only...")
        return run_relevance_checker_tests()
    elif agent_name in ["research", "research_agent"]:
        print("Running ResearchAgent tests only...")
        return run_research_agent_tests()
    elif agent_name in ["verification", "verification_agent"]:
        print("Running VerificationAgent tests only...")
        return run_verification_agent_tests()
    elif agent_name in ["builder", "retriever", "retriever_builder"]:
        print("Running RetrieverBuilder tests only...")
        return run_retriever_builder_tests()
    else:
        print(f"❌ Unknown agent: {agent_name}")
        print("Available agents: relevance, research, verification, builder")
        return False


def main():
    """Main entry point for the test runner."""
    if len(sys.argv) > 1:
        # Run specific agent test
        agent_name = sys.argv[1]
        success = run_specific_agent_test(agent_name)
    else:
        # Run all tests
        success = run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
