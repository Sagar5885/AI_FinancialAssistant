"""
Streamlit web interface for AI Finance Assistant
"""
import streamlit as st
import logging
import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Add project root to Python path to fix imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
    }
    .message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize Streamlit session state"""
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {}
    if 'goals' not in st.session_state:
        st.session_state.goals = []
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{datetime.now().timestamp()}"
    if 'manager' not in st.session_state:
        st.session_state.manager = None


def load_agents():
    """Load and initialize all agents"""
    try:
        logger.info("Starting agent initialization...")
        from src.core.llm_client import LLMClient
        logger.info("✓ Imported LLMClient")
        
        from src.rag.rag_system import KnowledgeBase, RAGRetriever
        logger.info("✓ Imported RAG modules")
        
        from src.utils.market_data import MarketDataProvider
        logger.info("✓ Imported MarketDataProvider")
        
        from src.agents.finance_qa_agent import FinanceQAAgent
        from src.agents.portfolio_analysis_agent import PortfolioAnalysisAgent
        from src.agents.market_analysis_agent import MarketAnalysisAgent
        from src.agents.goal_planning_agent import GoalPlanningAgent
        from src.agents.news_synthesizer_agent import NewsSynthesizerAgent
        from src.agents.tax_education_agent import TaxEducationAgent
        logger.info("✓ Imported all agents")
        
        from src.workflow.langgraph_workflow import (
            WorkflowRouter,
            ConversationManager,
            AgentType
        )
        logger.info("✓ Imported workflow modules")

        # Initialize LLM client
        api_key = os.getenv('GOOGLE_API_KEY', '')
        if not api_key:
            logger.error("GOOGLE_API_KEY not set!")
            st.error("ERROR: GOOGLE_API_KEY environment variable not set")
            return None
            
        logger.info("Initializing LLM client with Gemini...")
        llm_client = LLMClient(provider='gemini', api_key=api_key)
        logger.info("✓ LLM client initialized")

        # Initialize knowledge base and RAG
        logger.info("Initializing knowledge base...")
        kb = KnowledgeBase()
        logger.info("✓ Knowledge base initialized")
        
        logger.info("Initializing RAG retriever...")
        rag_retriever = RAGRetriever(kb)
        logger.info("✓ RAG retriever initialized")

        # Initialize market data provider
        logger.info("Initializing market data provider...")
        market_provider = MarketDataProvider(provider='yfinance')
        logger.info("✓ Market data provider initialized")

        # Initialize agents
        logger.info("Initializing specialized agents...")
        agents = {
            AgentType.FINANCE_QA: FinanceQAAgent(llm_client, rag_retriever),
            AgentType.PORTFOLIO_ANALYSIS: PortfolioAnalysisAgent(
                llm_client, rag_retriever, market_provider
            ),
            AgentType.MARKET_ANALYSIS: MarketAnalysisAgent(
                llm_client, rag_retriever, market_provider
            ),
            AgentType.GOAL_PLANNING: GoalPlanningAgent(
                llm_client, rag_retriever
            ),
            AgentType.NEWS_SYNTHESIZER: NewsSynthesizerAgent(
                llm_client, rag_retriever
            ),
            AgentType.TAX_EDUCATION: TaxEducationAgent(
                llm_client, rag_retriever
            ),
        }
        logger.info("✓ All agents initialized")

        # Initialize router and conversation manager
        logger.info("Initializing workflow router...")
        router = WorkflowRouter(agents, llm_client)
        logger.info("✓ Router initialized")
        
        logger.info("Initializing conversation manager...")
        manager = ConversationManager(router)
        logger.info("✓ Conversation manager initialized")
        
        logger.info("✅ All systems initialized successfully!")
        return manager

    except Exception as e:
        logger.error(f"❌ Error loading agents: {e}", exc_info=True)
        st.error(f"Failed to initialize agents: {str(e)}")
        return None


def display_conversation():
    """Display conversation history"""
    for message in st.session_state.conversation:
        if message['role'] == 'user':
            st.markdown(
                f"<div class='message user-message'><b>You:</b> {message['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='message assistant-message'><b>Assistant:</b> {message['content']}</div>",
                unsafe_allow_html=True
            )


def render_home_tab():
    """Render home/welcome tab"""
    st.title("💰 AI Finance Assistant")
    st.markdown("""
    Welcome to your personal AI Finance Assistant! This application provides:
    
    - **Financial Education**: Learn about investing, stocks, bonds, and more
    - **Portfolio Analysis**: Get insights on your investment portfolio
    - **Market Analysis**: Stay updated with real-time market data
    - **Goal Planning**: Plan your financial goals and retirement
    - **Tax Education**: Understand tax-advantaged accounts
    - **News Synthesis**: Get financial news contextualized for investors
    
    ### How to Use:
    1. Go to the "Chat" tab to start asking questions
    2. Use the "Portfolio" tab to enter and analyze your holdings
    3. Set goals in the "Goals" tab
    4. Check market data in the "Markets" tab
    
    ### Getting Started:
    Start by asking any financial question or describing your situation!
    """)

    # Display quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Portfolio Holdings", len(st.session_state.portfolio))
    with col2:
        st.metric("Financial Goals", len(st.session_state.goals))
    with col3:
        st.metric("Messages", len(st.session_state.conversation))


def render_chat_tab():
    """Render main chat interface"""
    st.title("💬 Chat with AI Finance Assistant")

    # Display conversation history
    display_conversation()

    # Input area
    st.markdown("---")
    user_input = st.text_input(
        "Ask me anything about finance:",
        placeholder="e.g., 'Explain what stocks are' or 'Analyze my portfolio' or 'What's happening in the market?'"
    )

    if user_input:
        if st.session_state.manager:
            with st.spinner("Processing your request..."):
                response = st.session_state.manager.process_message(
                    st.session_state.user_id,
                    user_input
                )

                # Add to conversation
                st.session_state.conversation.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.conversation.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().isoformat()
                })

                # Rerun to display new messages
                st.rerun()
        else:
            st.error("Chat system not initialized. Please refresh the page.")


def render_portfolio_tab():
    """Render portfolio management tab"""
    st.title("📊 Portfolio Management")

    st.markdown("### Your Holdings")

    col1, col2 = st.columns([2, 1])

    with col1:
        symbol = st.text_input("Stock Symbol (e.g., AAPL):", key="symbol_input")
        quantity = st.number_input("Quantity:", min_value=0.0, value=0.0, key="qty_input")

    with col2:
        if st.button("Add to Portfolio"):
            if symbol and quantity > 0:
                st.session_state.portfolio[symbol] = quantity
                st.success(f"Added {quantity} shares of {symbol}")
                st.rerun()

    # Display current portfolio
    if st.session_state.portfolio:
        st.markdown("### Current Portfolio")
        portfolio_data = []
        for symbol, quantity in st.session_state.portfolio.items():
            portfolio_data.append({
                'Symbol': symbol,
                'Quantity': quantity,
                'Action': '❌'
            })

        for symbol in st.session_state.portfolio:
            if st.button(f"Remove {symbol}", key=f"remove_{symbol}"):
                del st.session_state.portfolio[symbol]
                st.rerun()

        import pandas as pd
        df = pd.DataFrame(portfolio_data)
        st.dataframe(df, use_container_width=True)

        # Analyze button
        if st.button("Analyze My Portfolio"):
            manager = st.session_state.manager
            if manager:
                query = "Analyze my portfolio and provide insights on diversification and risk."
                with st.spinner("Analyzing your portfolio..."):
                    response = manager.process_message(
                        st.session_state.user_id,
                        query
                    )
                    st.session_state.conversation.append({
                        'role': 'user',
                        'content': query
                    })
                    st.session_state.conversation.append({
                        'role': 'assistant',
                        'content': response
                    })
                    st.success("Analysis complete!")
                    st.markdown(response)


def render_goals_tab():
    """Render financial goals tab"""
    st.title("🎯 Financial Goals")

    st.markdown("### Set Your Financial Goals")

    goal_type = st.selectbox(
        "Goal Type:",
        ["Retirement", "Home Purchase", "College Fund", "Emergency Fund", "Vacation", "Other"]
    )

    goal_amount = st.number_input("Target Amount ($):", min_value=0.0, value=100000.0)
    timeframe = st.number_input("Timeframe (Years):", min_value=1, value=10)
    risk_tolerance = st.selectbox("Risk Tolerance:", ["Conservative", "Moderate", "Aggressive"])

    if st.button("Create Goal"):
        goal = {
            'type': goal_type,
            'amount': goal_amount,
            'timeframe': timeframe,
            'risk_tolerance': risk_tolerance,
            'created': datetime.now().isoformat()
        }
        st.session_state.goals.append(goal)
        st.success(f"Goal created: {goal_type} of ${goal_amount:,.2f} in {timeframe} years")
        st.rerun()

    # Display goals
    if st.session_state.goals:
        st.markdown("### Your Goals")
        for idx, goal in enumerate(st.session_state.goals):
            with st.expander(f"{goal['type']} - ${goal['amount']:,.2f} in {goal['timeframe']} years"):
                st.write(f"**Risk Tolerance:** {goal['risk_tolerance']}")
                st.write(f"**Created:** {goal['created']}")

                # Get planning advice
                if st.button(f"Get Planning Advice", key=f"goal_{idx}"):
                    manager = st.session_state.manager
                    if manager:
                        query = f"Help me plan for my {goal['type']} goal of ${goal['amount']:,.2f} in {goal['timeframe']} years with {goal['risk_tolerance']} risk tolerance."
                        with st.spinner("Generating plan..."):
                            response = manager.process_message(
                                st.session_state.user_id,
                                query
                            )
                            st.markdown(response)


def render_markets_tab():
    """Render market overview tab"""
    st.title("📈 Market Overview")

    st.markdown("### Market Status")

    try:
        from src.utils.market_data import MarketDataProvider
        market_provider = MarketDataProvider(provider='yfinance')
        trends = market_provider.get_market_trends()

        if trends:
            market_cols = st.columns(len(trends))
            for idx, trend in enumerate(trends):
                with market_cols[idx]:
                    st.metric(
                        trend.index,
                        f"{trend.value:.2f}",
                        f"{trend.change_percent:+.2f}%"
                    )
        else:
            st.info("Market data currently unavailable")

    except Exception as e:
        st.warning(f"Could not fetch market data: {str(e)}")

    # Stock lookup
    st.markdown("### Stock Lookup")
    lookup_symbol = st.text_input("Enter stock symbol (e.g., AAPL):")

    if lookup_symbol:
        try:
            from src.utils.market_data import MarketDataProvider
            logger.info(f"Fetching data for {lookup_symbol}...")
            market_provider = MarketDataProvider(provider='yfinance')
            quote = market_provider.get_stock_quote(lookup_symbol.upper())

            if quote:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"{quote.symbol}", f"${quote.price:.2f}")
                with col2:
                    st.metric("Change", f"{quote.change_percent:+.2f}%")
                with col3:
                    st.metric("Currency", quote.currency)
                logger.info(f"✓ Successfully fetched {lookup_symbol}")
            else:
                st.error(f"No data found for {lookup_symbol}")

        except ImportError as ie:
            logger.error(f"Import error: {ie}", exc_info=True)
            st.error(f"Module import error: {str(ie)}")
        except Exception as e:
            logger.error(f"Error fetching data: {e}", exc_info=True)
            st.error(f"Error fetching data: {str(e)}")


def main():
    """Main app function"""
    init_session_state()

    # Load agents on first run
    if st.session_state.manager is None:
        with st.spinner("Initializing AI agents..."):
            st.session_state.manager = load_agents()

    # Sidebar
    with st.sidebar:
        st.title("📱 Navigation")
        st.markdown("---")

        # Session info
        if st.session_state.manager:
            st.success("✅ System Ready")
        else:
            st.error("❌ System Initialization Failed")

        st.markdown("---")

        # Clear session button
        if st.button("🔄 Clear Session"):
            st.session_state.conversation = []
            st.session_state.portfolio = {}
            st.session_state.goals = []
            st.rerun()

        st.markdown("---")
        st.markdown("### Tips:")
        st.markdown("""
        - Ask questions naturally
        - Update your portfolio for analysis
        - Set goals for planning help
        - Check markets regularly
        """)

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Home",
        "💬 Chat",
        "📊 Portfolio",
        "🎯 Goals",
        "📈 Markets"
    ])

    with tab1:
        render_home_tab()

    with tab2:
        render_chat_tab()

    with tab3:
        render_portfolio_tab()

    with tab4:
        render_goals_tab()

    with tab5:
        render_markets_tab()


if __name__ == "__main__":
    main()
