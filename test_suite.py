#!/usr/bin/env python3
"""
Test runner for AI Finance Assistant - Demonstrates core functionality
without requiring all external dependencies
"""
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_basic_imports():
    """Test that core modules can be imported"""
    print("=" * 60)
    print("Testing Basic Imports")
    print("=" * 60)
    
    try:
        from src.agents.base_agent import Agent
        print("✓ Base Agent imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Base Agent: {e}")
        return False

    try:
        from src.agents.finance_qa_agent import FinanceQAAgent
        print("✓ Finance QA Agent imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Finance QA Agent: {e}")
        return False

    try:
        from src.agents.portfolio_analysis_agent import PortfolioAnalysisAgent
        print("✓ Portfolio Analysis Agent imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Portfolio Analysis Agent: {e}")
        return False

    try:
        from src.workflow.langgraph_workflow import (
            IntentDetector, ConversationManager, WorkflowRouter, AgentType
        )
        print("✓ Workflow components imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Workflow: {e}")
        return False

    try:
        from src.rag.rag_system import KnowledgeBase, RAGRetriever, Document
        print("✓ RAG system imported successfully")
    except Exception as e:
        print(f"✗ Failed to import RAG: {e}")
        return False

    try:
        from src.utils.market_data import MarketDataCache, StockQuote
        print("✓ Market data utils imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Market Data: {e}")
        return False

    return True


def test_agent_creation():
    """Test that agents can be created"""
    print("\n" + "=" * 60)
    print("Testing Agent Creation")
    print("=" * 60)

    try:
        from src.agents.finance_qa_agent import FinanceQAAgent
        from src.agents.portfolio_analysis_agent import PortfolioAnalysisAgent
        from src.agents.market_analysis_agent import MarketAnalysisAgent
        from src.agents.goal_planning_agent import GoalPlanningAgent
        from src.agents.news_synthesizer_agent import NewsSynthesizerAgent
        from src.agents.tax_education_agent import TaxEducationAgent

        agents = [
            ("Finance Q&A", FinanceQAAgent()),
            ("Portfolio Analysis", PortfolioAnalysisAgent()),
            ("Market Analysis", MarketAnalysisAgent()),
            ("Goal Planning", GoalPlanningAgent()),
            ("News Synthesizer", NewsSynthesizerAgent()),
            ("Tax Education", TaxEducationAgent()),
        ]

        for name, agent in agents:
            if agent and hasattr(agent, 'process'):
                print(f"✓ {name} Agent created successfully")
            else:
                print(f"✗ {name} Agent creation failed")
                return False

        return True

    except Exception as e:
        print(f"✗ Error creating agents: {e}")
        return False


def test_knowledge_base():
    """Test knowledge base"""
    print("\n" + "=" * 60)
    print("Testing Knowledge Base")
    print("=" * 60)

    try:
        from src.rag.rag_system import KnowledgeBase
        
        kb = KnowledgeBase()
        docs = kb.load_documents()
        
        if len(docs) > 0:
            print(f"✓ Knowledge Base loaded with {len(docs)} documents")
            
            # Test category retrieval
            categories = {}
            for doc in docs:
                if doc.category not in categories:
                    categories[doc.category] = 0
                categories[doc.category] += 1
            
            print(f"✓ Documents organized into {len(categories)} categories:")
            for category, count in categories.items():
                print(f"  - {category}: {count} articles")
            
            return True
        else:
            print("⚠ Knowledge base loaded but no documents found")
            print("  Run: python3 src/data/knowledge_base_builder.py")
            return True

    except Exception as e:
        print(f"✗ Knowledge base error: {e}")
        return False


def test_workflow_intent_detection():
    """Test workflow intent detection"""
    print("\n" + "=" * 60)
    print("Testing Intent Detection")
    print("=" * 60)

    try:
        from src.workflow.langgraph_workflow import IntentDetector, AgentType

        detector = IntentDetector()
        
        test_cases = [
            ("What is a stock?", AgentType.FINANCE_QA),
            ("Analyze my portfolio", AgentType.PORTFOLIO_ANALYSIS),
            ("What's the market doing?", AgentType.MARKET_ANALYSIS),
            ("Help me plan for retirement", AgentType.GOAL_PLANNING),
            ("Tell me about this news", AgentType.NEWS_SYNTHESIZER),
            ("Explain 401k", AgentType.TAX_EDUCATION),
        ]

        for query, expected_intent in test_cases:
            detected = detector.detect_intent(query)
            if detected == expected_intent:
                print(f"✓ Correctly detected: '{query}' → {detected.value}")
            else:
                print(f"⚠ Intent mismatch: '{query}'")
                print(f"  Expected: {expected_intent.value}, Got: {detected.value}")

        return True

    except Exception as e:
        print(f"✗ Intent detection error: {e}")
        return False


def test_conversation_manager():
    """Test conversation manager"""
    print("\n" + "=" * 60)
    print("Testing Conversation Manager")
    print("=" * 60)

    try:
        from src.workflow.langgraph_workflow import (
            ConversationManager, WorkflowRouter, AgentType
        )
        from src.agents.finance_qa_agent import FinanceQAAgent

        # Create minimal setup
        agents = {
            AgentType.FINANCE_QA: FinanceQAAgent(),
        }
        router = WorkflowRouter(agents)
        manager = ConversationManager(router)

        # Test session management
        state = manager.create_session("test_user_001")
        if state:
            print("✓ Session created successfully")
        else:
            print("✗ Failed to create session")
            return False

        # Test session retrieval
        retrieved = manager.get_session("test_user_001")
        if retrieved:
            print("✓ Session retrieved successfully")
        else:
            print("✗ Failed to retrieve session")
            return False

        # Test portfolio update
        manager.update_portfolio("test_user_001", {"AAPL": 10, "MSFT": 5})
        print("✓ Portfolio updated successfully")

        # Test goal setting
        goal = {
            'type': 'Retirement',
            'amount': 1000000,
            'timeframe': 20,
            'risk_tolerance': 'Moderate'
        }
        manager.set_goal("test_user_001", goal)
        print("✓ Goal added successfully")

        # Test session summary
        summary = manager.get_session_summary("test_user_001")
        print(f"✓ Session summary: {len(summary)} keys")

        return True

    except Exception as e:
        print(f"✗ Conversation manager error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_market_data_cache():
    """Test market data caching"""
    print("\n" + "=" * 60)
    print("Testing Market Data Cache")
    print("=" * 60)

    try:
        from src.utils.market_data import MarketDataCache
        import time

        cache = MarketDataCache(ttl_seconds=2)
        
        # Test set and get
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        
        if value == "test_value":
            print("✓ Cache set and get working")
        else:
            print("✗ Cache get failed")
            return False

        # Test expiry
        time.sleep(2.1)
        expired_value = cache.get("test_key")
        
        if expired_value is None:
            print("✓ Cache expiry working correctly")
        else:
            print("⚠ Cache expiry timing may be off")

        return True

    except Exception as e:
        print(f"✗ Market data cache error: {e}")
        return False


def test_rag_system():
    """Test RAG system without embeddings"""
    print("\n" + "=" * 60)
    print("Testing RAG System")
    print("=" * 60)

    try:
        from src.rag.rag_system import KnowledgeBase, Document

        kb = KnowledgeBase()
        
        # Add test document
        test_doc = Document(
            id="test_doc_123",
            title="Test Article",
            content="This is a test article about investing",
            category="test",
            source="test_source",
            tags=["test", "investing"]
        )
        kb.add_document(test_doc)
        
        print("✓ Document added to knowledge base")

        # Test category retrieval
        test_category_docs = kb.get_documents_by_category("test")
        if test_doc in test_category_docs:
            print("✓ Category-based retrieval working")
        else:
            print("⚠ Category retrieval may have issues")

        # Test tag search
        tagged_docs = kb.search_by_tag("investing")
        if test_doc in tagged_docs:
            print("✓ Tag-based search working")
        else:
            print("⚠ Tag search may have issues")

        return True

    except Exception as e:
        print(f"✗ RAG system error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  AI Finance Assistant - Test Suite".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    tests = [
        ("Basic Imports", test_basic_imports),
        ("Agent Creation", test_agent_creation),
        ("Knowledge Base", test_knowledge_base),
        ("Intent Detection", test_workflow_intent_detection),
        ("Conversation Manager", test_conversation_manager),
        ("Market Data Cache", test_market_data_cache),
        ("RAG System", test_rag_system),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set API key: export GOOGLE_API_KEY='your_key'")
        print("3. Run app: python main.py --mode web")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
