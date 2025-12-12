"""
Workflow orchestration using LangGraph for agent routing and state management
"""
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Supported agent types"""
    FINANCE_QA = "finance_qa"
    PORTFOLIO_ANALYSIS = "portfolio_analysis"
    MARKET_ANALYSIS = "market_analysis"
    GOAL_PLANNING = "goal_planning"
    NEWS_SYNTHESIZER = "news_synthesizer"
    TAX_EDUCATION = "tax_education"


@dataclass
class WorkflowState:
    """Maintains state throughout workflow execution"""
    user_id: str
    messages: List[Dict[str, Any]]
    current_agent: Optional[AgentType] = None
    context: Dict[str, Any] = None
    portfolio: Dict[str, float] = None
    goals: List[Dict[str, Any]] = None
    preferences: Dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.portfolio is None:
            self.portfolio = {}
        if self.goals is None:
            self.goals = []
        if self.preferences is None:
            self.preferences = {}

    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation history"""
        self.messages.append({
            'role': role,
            'content': content,
            'timestamp': self._get_timestamp()
        })

    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        return self.messages[-limit:]

    def update_context(self, key: str, value: Any) -> None:
        """Update workflow context"""
        self.context[key] = value

    @staticmethod
    def _get_timestamp():
        from datetime import datetime
        return datetime.now().isoformat()


class IntentDetector:
    """Detects user intent and routes to appropriate agent"""

    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.intent_keywords = self._build_intent_keywords()

    def _build_intent_keywords(self) -> Dict[AgentType, List[str]]:
        """Build keyword mappings for intent detection"""
        return {
            AgentType.FINANCE_QA: [
                'explain', 'what is', 'how does', 'teach', 'learn', 'understand',
                'definition', 'concept', 'meaning', 'question', 'tell me'
            ],
            AgentType.PORTFOLIO_ANALYSIS: [
                'portfolio', 'holdings', 'investment', 'analyze', 'review',
                'diversification', 'allocation', 'rebalance', 'performance'
            ],
            AgentType.MARKET_ANALYSIS: [
                'market', 'stock', 'trend', 'index', 'economic', 'outlook',
                'analysis', 'sentiment', 'news'
            ],
            AgentType.GOAL_PLANNING: [
                'goal', 'plan', 'save', 'retire', 'target', 'timeline',
                'objective', 'strategy', 'how much'
            ],
            AgentType.NEWS_SYNTHESIZER: [
                'news', 'event', 'impact', 'development', 'headlines',
                'current', 'recent', 'summary'
            ],
            AgentType.TAX_EDUCATION: [
                'tax', '401k', 'ira', 'roth', 'account', 'contribution',
                'deduction', 'form', 'filing'
            ]
        }

    def detect_intent(self, query: str) -> AgentType:
        """Detect user intent from query"""
        query_lower = query.lower()

        # Keyword-based detection
        for agent_type, keywords in self.intent_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return agent_type

        # Default to Finance Q&A
        return AgentType.FINANCE_QA

    def extract_context_from_query(self, query: str) -> Dict[str, Any]:
        """Extract relevant context from user query"""
        context = {}
        query_lower = query.lower()

        # Check for holdings/portfolio
        if any(word in query_lower for word in ['hold', 'own', 'portfolio', 'position']):
            context['needs_holdings'] = True

        # Check for goal information
        if any(word in query_lower for word in ['goal', 'save', 'retire', 'target']):
            context['needs_goals'] = True

        # Check for risk tolerance
        if any(word in query_lower for word in ['risk', 'conservative', 'aggressive', 'tolerance']):
            context['needs_risk_profile'] = True

        return context


class WorkflowRouter:
    """Routes messages to appropriate agents"""

    def __init__(self, agents: Dict[AgentType, Any], llm_client=None):
        self.agents = agents
        self.intent_detector = IntentDetector(llm_client)
        logger.info("WorkflowRouter initialized with agents")

    def route(self, query: str, state: WorkflowState) -> str:
        """Route query to appropriate agent and get response"""
        try:
            # Detect intent
            intent = self.intent_detector.detect_intent(query)
            state.current_agent = intent

            # Extract context
            context_hints = self.intent_detector.extract_context_from_query(query)
            state.update_context('hints', context_hints)

            # Merge context
            agent_context = {**state.context, **state.portfolio, **{'goals': state.goals}}

            # Get appropriate agent
            agent = self.agents.get(intent)
            if not agent:
                return f"Agent for {intent.value} not configured"

            # Process query
            logger.info(f"Routing to {intent.value} agent")
            response = agent.process(query, context=agent_context)

            # Store in state
            state.add_message('user', query)
            state.add_message('assistant', response)

            return response

        except Exception as e:
            logger.error(f"Error in workflow routing: {e}")
            return f"Error processing request: {str(e)}"


class ConversationManager:
    """Manages conversation flow and memory"""

    def __init__(self, router: WorkflowRouter):
        self.router = router
        self.sessions: Dict[str, WorkflowState] = {}

    def create_session(self, user_id: str) -> WorkflowState:
        """Create new conversation session"""
        state = WorkflowState(
            user_id=user_id,
            messages=[],
            context={},
            portfolio={},
            goals=[],
            preferences={}
        )
        self.sessions[user_id] = state
        logger.info(f"Created session for user: {user_id}")
        return state

    def get_session(self, user_id: str) -> Optional[WorkflowState]:
        """Get existing session"""
        return self.sessions.get(user_id)

    def process_message(self, user_id: str, message: str) -> str:
        """Process user message and return response"""
        state = self.get_session(user_id)
        if not state:
            state = self.create_session(user_id)

        return self.router.route(message, state)

    def update_portfolio(self, user_id: str, holdings: Dict[str, float]) -> None:
        """Update user's portfolio holdings"""
        state = self.get_session(user_id)
        if state:
            state.portfolio = holdings
            logger.info(f"Updated portfolio for user {user_id}")

    def set_goal(self, user_id: str, goal: Dict[str, Any]) -> None:
        """Add financial goal for user"""
        state = self.get_session(user_id)
        if state:
            state.goals.append(goal)
            logger.info(f"Added goal for user {user_id}")

    def clear_session(self, user_id: str) -> None:
        """Clear user session"""
        if user_id in self.sessions:
            del self.sessions[user_id]
            logger.info(f"Cleared session for user {user_id}")

    def get_conversation_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get conversation history for user"""
        state = self.get_session(user_id)
        if state:
            return state.get_conversation_history(limit)
        return []

    def get_session_summary(self, user_id: str) -> Dict[str, Any]:
        """Get session summary"""
        state = self.get_session(user_id)
        if not state:
            return {}

        return {
            'user_id': user_id,
            'messages_count': len(state.messages),
            'portfolio': state.portfolio,
            'goals': state.goals,
            'current_agent': state.current_agent.value if state.current_agent else None,
            'context_keys': list(state.context.keys())
        }
