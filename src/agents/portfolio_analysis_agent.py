"""
Portfolio Analysis Agent - Analyzes user portfolios and provides insights
"""
import logging
from typing import Dict, Any, Optional
from src.agents.base_agent import Agent

logger = logging.getLogger(__name__)


class PortfolioAnalysisAgent(Agent):
    """Analyzes investment portfolios and provides recommendations"""

    def __init__(self, llm_client=None, rag_retriever=None, market_provider=None):
        super().__init__(
            name="Portfolio Analysis Agent",
            description="Analyzes user investment portfolios and provides diversification insights",
            llm_client=llm_client,
            rag_retriever=rag_retriever
        )
        self.market_provider = market_provider

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Analyze portfolio"""
        try:
            holdings = context.get('holdings', {}) if context else {}
            
            if not holdings:
                return "Please provide your portfolio holdings in the format: {symbol: quantity, ...}"

            # Get market data for holdings
            portfolio_data = {}
            if self.market_provider:
                portfolio_data = self.market_provider.get_portfolio_performance(holdings)

            # Retrieve knowledge base articles on portfolio management
            kb_context = self.retrieve_context("portfolio diversification risk management", top_k=5)

            # Build analysis prompt
            portfolio_summary = self._summarize_portfolio(holdings, portfolio_data)

            prompt = f"""You are a portfolio analyst. Provide insights on the following portfolio:

Portfolio Summary:
{portfolio_summary}

Query: {query}

Analysis Guidelines:
- Assess diversification level
- Identify concentration risks
- Suggest improvements based on general principles (not specific recommendations)
- Consider sector allocation
- Mention tax-loss harvesting opportunities
- Always include risk disclaimers

Provide constructive analysis."""

            response = self.generate_response(prompt, context=kb_context)

            self.add_to_memory({
                'type': 'portfolio_analysis',
                'holdings': holdings,
                'response': response
            })

            return response

        except Exception as e:
            logger.error(f"Error in Portfolio Analysis Agent: {e}")
            return f"Error analyzing portfolio: {str(e)}"

    @staticmethod
    def _summarize_portfolio(holdings: Dict[str, float], portfolio_data: Dict[str, Any]) -> str:
        """Create summary of portfolio"""
        if not portfolio_data or not portfolio_data.get('holdings'):
            summary = "Holdings: " + ", ".join([f"{sym}: {qty}" for sym, qty in holdings.items()])
        else:
            summary = f"Total Portfolio Value: ${portfolio_data.get('total_value', 0):,.2f}\n\nHoldings:\n"
            for holding in portfolio_data.get('holdings', []):
                summary += f"- {holding['symbol']}: {holding['quantity']} shares @ ${holding['price']:.2f} (${holding['value']:,.2f})\n"

        return summary
