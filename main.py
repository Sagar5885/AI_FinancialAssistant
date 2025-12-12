#!/usr/bin/env python
"""
Main entry point for AI Finance Assistant
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_knowledge_base():
    """Initialize knowledge base"""
    try:
        from src.data.knowledge_base_builder import create_knowledge_base
        logger.info("Setting up knowledge base...")
        create_knowledge_base()
        logger.info("Knowledge base ready!")
    except Exception as e:
        logger.warning(f"Could not initialize knowledge base: {e}")


def run_streamlit_app():
    """Run Streamlit web interface"""
    try:
        import subprocess
        logger.info("Starting Streamlit app...")
        app_path = Path(__file__).parent / "src" / "web_app" / "streamlit_app.py"
        subprocess.run([
            "streamlit", "run",
            str(app_path),
            "--logger.level=info"
        ])
    except Exception as e:
        logger.error(f"Error running Streamlit app: {e}")
        sys.exit(1)


def run_cli_demo():
    """Run CLI demo"""
    try:
        from src.core.llm_client import LLMClient
        from src.rag.rag_system import KnowledgeBase, RAGRetriever
        from src.utils.market_data import MarketDataProvider
        from src.agents.finance_qa_agent import FinanceQAAgent
        from src.workflow.langgraph_workflow import IntentDetector, ConversationManager, WorkflowRouter, AgentType

        logger.info("Starting AI Finance Assistant CLI Demo...")

        # Setup
        api_key = os.getenv('GOOGLE_API_KEY', '')
        if not api_key:
            print("⚠️  No GOOGLE_API_KEY set. Using mock responses.")
            print("Set GOOGLE_API_KEY environment variable for real LLM responses.\n")

        # Initialize components
        llm_client = LLMClient(provider='gemini', api_key=api_key) if api_key else None
        kb = KnowledgeBase()
        rag_retriever = RAGRetriever(kb) if api_key else None
        market_provider = MarketDataProvider(provider='yfinance')

        # Initialize agents
        from src.agents.portfolio_analysis_agent import PortfolioAnalysisAgent
        from src.agents.market_analysis_agent import MarketAnalysisAgent
        from src.agents.goal_planning_agent import GoalPlanningAgent
        from src.agents.news_synthesizer_agent import NewsSynthesizerAgent
        from src.agents.tax_education_agent import TaxEducationAgent

        agents = {
            AgentType.FINANCE_QA: FinanceQAAgent(llm_client, rag_retriever),
            AgentType.PORTFOLIO_ANALYSIS: PortfolioAnalysisAgent(llm_client, rag_retriever, market_provider),
            AgentType.MARKET_ANALYSIS: MarketAnalysisAgent(llm_client, rag_retriever, market_provider),
            AgentType.GOAL_PLANNING: GoalPlanningAgent(llm_client, rag_retriever),
            AgentType.NEWS_SYNTHESIZER: NewsSynthesizerAgent(llm_client, rag_retriever),
            AgentType.TAX_EDUCATION: TaxEducationAgent(llm_client, rag_retriever),
        }

        # Create conversation manager
        router = WorkflowRouter(agents, llm_client)
        manager = ConversationManager(router)

        # Welcome message
        print("\n" + "="*60)
        print("💰 AI Finance Assistant - Interactive Demo")
        print("="*60)
        print("\nWelcome! I'm your AI Finance Assistant.")
        print("I can help with:")
        print("  • Financial education (stocks, bonds, investing)")
        print("  • Portfolio analysis")
        print("  • Market insights")
        print("  • Goal planning")
        print("  • Tax education")
        print("  • Financial news analysis")
        print("\nType 'exit' to quit, 'help' for examples\n")

        # Interactive loop
        user_id = "demo_user"
        manager.create_session(user_id)

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() == 'exit':
                    print("\nThank you for using AI Finance Assistant!")
                    break

                if user_input.lower() == 'help':
                    print("""
Example queries:
  • "Explain what stocks are"
  • "How do I start investing?"
  • "What's the difference between stocks and bonds?"
  • "Analyze my portfolio: AAPL 10, MSFT 5"
  • "What are index funds?"
  • "How do I plan for retirement?"
  • "Explain 401k vs IRA"
  • "What's happening in the stock market?"
                    """)
                    continue

                if not user_input:
                    continue

                # Process message
                print("\nAssistant: Processing your request...\n")
                response = manager.process_message(user_id, user_input)
                print(f"Assistant: {response}\n")

            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error processing input: {e}")
                print(f"Error: {str(e)}\n")

    except Exception as e:
        logger.error(f"Error in CLI demo: {e}")
        print(f"Error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Finance Assistant")
    parser.add_argument(
        '--mode',
        choices=['web', 'cli', 'setup'],
        default='web',
        help='Run mode: web (Streamlit), cli (interactive), or setup'
    )

    args = parser.parse_args()

    try:
        if args.mode == 'setup':
            setup_knowledge_base()
            print("✅ Setup complete!")
        elif args.mode == 'web':
            setup_knowledge_base()
            run_streamlit_app()
        elif args.mode == 'cli':
            setup_knowledge_base()
            run_cli_demo()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
