"""
Finance Q&A Agent - Handles general financial education queries
"""
import logging
from typing import Dict, Any, Optional
from src.agents.base_agent import Agent

logger = logging.getLogger(__name__)


class FinanceQAAgent(Agent):
    """Handles general financial education and Q&A"""

    def __init__(self, llm_client=None, rag_retriever=None):
        super().__init__(
            name="Finance Q&A Agent",
            description="Provides comprehensive financial education and answers to general finance questions",
            llm_client=llm_client,
            rag_retriever=rag_retriever
        )

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process financial education queries"""
        try:
            # Retrieve relevant knowledge base articles
            kb_context = self.retrieve_context(query, top_k=5)

            # Build prompt
            prompt = f"""You are a financial education expert. Provide clear, jargon-free explanations of financial concepts.
            
Query: {query}

Guidelines:
- Explain concepts in simple terms
- Use examples when helpful
- Avoid recommending specific investments
- Include risk disclaimers where appropriate
- Cite your sources

Please provide a helpful and educational response."""

            # Generate response
            response = self.generate_response(prompt, context=kb_context)

            # Add to memory
            self.add_to_memory({
                'type': 'qa',
                'query': query,
                'response': response
            })

            return response

        except Exception as e:
            logger.error(f"Error in Finance Q&A Agent: {e}")
            return f"I encountered an error while processing your question: {str(e)}"
