"""
Goal Planning Agent - Assists with financial goal setting and planning
"""
import logging
from typing import Dict, Any, Optional
from src.agents.base_agent import Agent

logger = logging.getLogger(__name__)


class GoalPlanningAgent(Agent):
    """Assists with financial goal setting and planning"""

    def __init__(self, llm_client=None, rag_retriever=None):
        super().__init__(
            name="Goal Planning Agent",
            description="Helps users set and plan financial goals considering risk tolerance",
            llm_client=llm_client,
            rag_retriever=rag_retriever
        )

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process goal planning queries"""
        try:
            # Extract goal parameters from context
            goal_params = self._extract_goal_params(context)

            # Retrieve knowledge base articles on goal planning
            kb_context = self.retrieve_context("goal setting financial planning retirement investment strategy", top_k=5)

            # Build prompt
            prompt = f"""You are a financial goal planning advisor. Help the user plan their financial goals:

User Query: {query}

Goal Parameters:
{goal_params}

Planning Guidelines:
- Consider the user's risk tolerance
- Suggest appropriate time horizons
- Mention diversification strategies
- Include emergency fund recommendations
- Discuss regular contribution importance
- Tailor advice to their situation
- Always include risk disclaimers

Provide a thoughtful goal planning response."""

            response = self.generate_response(prompt, context=kb_context)

            self.add_to_memory({
                'type': 'goal_planning',
                'query': query,
                'goal_params': goal_params,
                'response': response
            })

            return response

        except Exception as e:
            logger.error(f"Error in Goal Planning Agent: {e}")
            return f"Error planning goals: {str(e)}"

    @staticmethod
    def _extract_goal_params(context: Optional[Dict[str, Any]]) -> str:
        """Extract goal planning parameters from context"""
        if not context:
            return "No specific parameters provided"

        params = []
        
        if 'goal_amount' in context:
            params.append(f"Target Amount: ${context['goal_amount']:,.2f}")
        
        if 'timeframe' in context:
            params.append(f"Timeframe: {context['timeframe']} years")
        
        if 'current_savings' in context:
            params.append(f"Current Savings: ${context['current_savings']:,.2f}")
        
        if 'monthly_contribution' in context:
            params.append(f"Monthly Contribution: ${context['monthly_contribution']:,.2f}")
        
        if 'risk_tolerance' in context:
            params.append(f"Risk Tolerance: {context['risk_tolerance']}")
        
        if 'goal_type' in context:
            params.append(f"Goal Type: {context['goal_type']}")

        return "\n".join(params) if params else "No specific parameters provided"
