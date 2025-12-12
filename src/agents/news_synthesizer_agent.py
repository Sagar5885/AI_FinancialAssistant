"""
News Synthesizer Agent - Summarizes and contextualizes financial news
"""
import logging
from typing import Dict, Any, Optional, List
from src.agents.base_agent import Agent

logger = logging.getLogger(__name__)


class NewsSynthesizerAgent(Agent):
    """Synthesizes and contextualizes financial news"""

    def __init__(self, llm_client=None, rag_retriever=None):
        super().__init__(
            name="News Synthesizer Agent",
            description="Summarizes financial news and contextualizes impact on investments",
            llm_client=llm_client,
            rag_retriever=rag_retriever
        )

    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process news synthesis queries"""
        try:
            # Extract news topics from context
            topics = context.get('topics', []) if context else []
            news_items = context.get('news_items', []) if context else []

            # Retrieve knowledge base articles on economic impacts
            kb_context = self.retrieve_context("economic news impact market sentiment financial events", top_k=5)

            # Build prompt
            news_summary = self._summarize_news_items(news_items)

            prompt = f"""You are a financial news analyst. Synthesize the following financial news and its potential impact:

Query: {query}

Topics of Interest: {', '.join(topics) if topics else 'General market news'}

News Summary:
{news_summary}

Analysis Guidelines:
- Explain key implications for investors
- Contextualize within broader economic trends
- Discuss potential sector impacts
- Mention affected asset classes
- Avoid predicting specific market movements
- Provide balanced perspective
- Include appropriate disclaimers

Provide a comprehensive news synthesis."""

            response = self.generate_response(prompt, context=kb_context)

            self.add_to_memory({
                'type': 'news_synthesis',
                'topics': topics,
                'query': query,
                'response': response
            })

            return response

        except Exception as e:
            logger.error(f"Error in News Synthesizer Agent: {e}")
            return f"Error synthesizing news: {str(e)}"

    @staticmethod
    def _summarize_news_items(news_items: List[Dict[str, Any]]) -> str:
        """Create summary of news items"""
        if not news_items:
            return "No specific news items provided. Provide news articles with titles and summaries."

        summary = ""
        for idx, item in enumerate(news_items, 1):
            summary += f"{idx}. {item.get('title', 'Untitled')}\n"
            if 'summary' in item:
                summary += f"   Summary: {item['summary']}\n"
            if 'date' in item:
                summary += f"   Date: {item['date']}\n"
            summary += "\n"

        return summary
