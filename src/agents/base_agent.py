"""
Base agent class for all specialized agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Agent(ABC):
    """Base class for all agents"""

    def __init__(self, name: str, description: str, llm_client=None, rag_retriever=None):
        self.name = name
        self.description = description
        self.llm_client = llm_client
        self.rag_retriever = rag_retriever
        self.memory: List[Dict[str, Any]] = []
        logger.info(f"Initialized agent: {name}")

    @abstractmethod
    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process user query and return response"""
        pass

    def add_to_memory(self, message: Dict[str, Any]) -> None:
        """Add message to agent memory"""
        message['timestamp'] = datetime.now()
        self.memory.append(message)

    def get_memory(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memory entries"""
        return self.memory[-limit:]

    def clear_memory(self) -> None:
        """Clear agent memory"""
        self.memory.clear()

    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """Retrieve relevant context from knowledge base"""
        if not self.rag_retriever:
            return ""
        
        try:
            retrieved_docs = self.rag_retriever.retrieve(query, top_k=top_k)
            if retrieved_docs:
                from src.rag.rag_system import RAGContext
                return RAGContext.build_context(retrieved_docs)
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
        
        return ""

    def generate_response(self, prompt: str, context: Optional[str] = None, **kwargs) -> str:
        """Generate response using LLM"""
        if not self.llm_client:
            return "LLM client not configured"

        try:
            if context:
                response = self.llm_client.generate_with_context(
                    prompt, context, **kwargs
                )
            else:
                response = self.llm_client.generate(prompt, **kwargs)
            
            logger.info(f"✓ Response generated successfully")
            return response
            
        except RuntimeError as e:
            error_msg = str(e)
            logger.error(f"LLM generation failed: {error_msg}")
            return f"Sorry, I'm experiencing technical difficulties: {error_msg}"
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Unexpected error generating response: {error_msg}")
            return f"Error: {error_msg}"
