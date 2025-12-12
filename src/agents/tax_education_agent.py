"""
Tax Education Agent - Explains tax concepts and account types
"""
import logging
from typing import Dict, Any, Optional
from src.agents.base_agent import Agent

logger = logging.getLogger(__name__)


class TaxEducationAgent(Agent):
    """Explains tax concepts and account types"""

    def __init__(self, llm_client=None, rag_retriever=None):
        super().__init__(
            name="Tax Education Agent",
            description="Educates users on tax concepts, account types, and tax-advantaged strategies",
            llm_client=llm_client,
            rag_retriever=rag_retriever
        )

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process tax education queries"""
        try:
            # Retrieve knowledge base articles on taxes and accounts
            kb_context = self.retrieve_context("taxes tax-advantaged accounts 401k IRA Roth traditional HSA", top_k=5)

            # Build prompt
            prompt = f"""You are a tax education expert. Provide clear explanations about taxes and investment accounts:

Query: {query}

Education Guidelines:
- Explain tax concepts in simple language
- Compare different account types
- Discuss tax-advantaged strategies
- Mention contribution limits (if applicable)
- Discuss withdrawal rules
- Include important disclaimers
- Note that this is educational only, not tax advice
- Recommend consulting a tax professional for specific situations

Provide helpful tax education."""

            response = self.generate_response(prompt, context=kb_context)

            # Add disclaimer
            response += "\n\n⚠️ DISCLAIMER: This is educational information only and not tax advice. Please consult with a qualified tax professional for your specific situation."

            self.add_to_memory({
                'type': 'tax_education',
                'query': query,
                'response': response
            })

            return response

        except Exception as e:
            logger.error(f"Error in Tax Education Agent: {e}")
            return f"Error providing tax education: {str(e)}"
