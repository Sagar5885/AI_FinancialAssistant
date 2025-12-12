"""
Market Analysis Agent - Provides real-time market insights
"""
import logging
from typing import Dict, Any, Optional
from src.agents.base_agent import Agent

logger = logging.getLogger(__name__)


class MarketAnalysisAgent(Agent):
    """Provides real-time market analysis and insights"""

    def __init__(self, llm_client=None, rag_retriever=None, market_provider=None):
        super().__init__(
            name="Market Analysis Agent",
            description="Analyzes market trends and provides real-time market insights",
            llm_client=llm_client,
            rag_retriever=rag_retriever
        )
        self.market_provider = market_provider

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Analyze market"""
        try:
            # Get market trends
            market_trends = []
            market_summary = "Market data currently unavailable"
            
            if self.market_provider:
                market_trends = self.market_provider.get_market_trends()
                market_summary = self._summarize_market_trends(market_trends)

            # Retrieve knowledge base articles on market analysis
            kb_context = self.retrieve_context("market trends technical analysis economic indicators", top_k=5)

            # Build analysis prompt
            prompt = f"""You are a market analyst. Provide insights on current market conditions:

Current Market Status:
{market_summary}

User Query: {query}

Analysis Guidelines:
- Explain current market conditions in simple terms
- Discuss major market drivers
- Mention relevant economic indicators
- Avoid making specific stock predictions
- Include appropriate disclaimers
- Contextualize short-term volatility with long-term trends

Provide balanced market analysis."""

            response = self.generate_response(prompt, context=kb_context)

            self.add_to_memory({
                'type': 'market_analysis',
                'query': query,
                'response': response
            })

            return response

        except Exception as e:
            logger.error(f"Error in Market Analysis Agent: {e}")
            return f"Error analyzing market: {str(e)}"

    @staticmethod
    def _summarize_market_trends(trends) -> str:
        """Create summary of market trends"""
        if not trends:
            return "Market indices data not currently available"
        
        summary = "Market Indices:\n"
        for trend in trends:
            direction = "📈" if trend.change_percent > 0 else "📉"
            summary += f"- {trend.index}: {trend.value:.2f} ({trend.change_percent:+.2f}%) {direction}\n"
        
        return summary
