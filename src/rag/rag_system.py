"""
RAG (Retrieval-Augmented Generation) system for financial knowledge base
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Represents a knowledge base document"""
    id: str
    title: str
    content: str
    category: str
    source: str
    tags: List[str]


class KnowledgeBase:
    """Manages financial knowledge base documents"""

    def __init__(self, kb_path: Optional[str] = None):
        self.documents: List[Document] = []
        self.kb_path = kb_path or Path(__file__).parent.parent / "data" / "knowledge_base"
        self._ensure_kb_exists()

    def _ensure_kb_exists(self):
        """Ensure knowledge base directory exists"""
        Path(self.kb_path).mkdir(parents=True, exist_ok=True)

    def load_documents(self) -> List[Document]:
        """Load documents from knowledge base"""
        kb_dir = Path(self.kb_path)
        for json_file in kb_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for doc_data in data:
                            self.documents.append(
                                Document(
                                    id=doc_data.get('id'),
                                    title=doc_data.get('title'),
                                    content=doc_data.get('content'),
                                    category=doc_data.get('category'),
                                    source=doc_data.get('source'),
                                    tags=doc_data.get('tags', [])
                                )
                            )
                    else:
                        self.documents.append(
                            Document(
                                id=data.get('id'),
                                title=data.get('title'),
                                content=data.get('content'),
                                category=data.get('category'),
                                source=data.get('source'),
                                tags=data.get('tags', [])
                            )
                        )
            except Exception as e:
                logger.warning(f"Failed to load document from {json_file}: {e}")

        logger.info(f"Loaded {len(self.documents)} documents from knowledge base")
        return self.documents

    def add_document(self, doc: Document) -> None:
        """Add a document to knowledge base"""
        self.documents.append(doc)

    def get_documents_by_category(self, category: str) -> List[Document]:
        """Get documents by category"""
        return [doc for doc in self.documents if doc.category.lower() == category.lower()]

    def search_by_tag(self, tag: str) -> List[Document]:
        """Search documents by tag"""
        return [doc for doc in self.documents if tag.lower() in [t.lower() for t in doc.tags]]


class RAGRetriever:
    """Retrieves relevant documents using vector similarity"""

    def __init__(self, kb: KnowledgeBase, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            self.transformer = SentenceTransformer(embedding_model)
            self.faiss = faiss
            self.kb = kb
            self.index = None
            self.documents = []
            self._build_index()
            logger.info("RAG Retriever initialized successfully")
        except ImportError as e:
            logger.warning(f"Missing required packages for RAG: {e}. Using fallback retrieval.")
            self.transformer = None
            self.faiss = None
            self.kb = kb

    def _build_index(self) -> None:
        """Build FAISS index from documents"""
        if not self.transformer or not self.faiss:
            return

        self.documents = self.kb.load_documents()
        if not self.documents:
            logger.warning("No documents available to build index")
            return

        texts = [doc.content for doc in self.documents]
        embeddings = self.transformer.encode(texts, convert_to_tensor=True)
        
        # Build FAISS index
        import numpy as np
        embeddings_np = embeddings.cpu().numpy().astype('float32')
        self.index = self.faiss.IndexFlatL2(embeddings_np.shape[1])
        self.index.add(embeddings_np)
        logger.info(f"Built FAISS index with {len(self.documents)} documents")

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        """Retrieve top-k most relevant documents"""
        if not self.transformer or not self.index or not self.documents:
            # Fallback: return all documents
            return [(doc, 0.0) for doc in self.documents[:top_k]]

        try:
            query_embedding = self.transformer.encode([query], convert_to_tensor=True)
            import numpy as np
            query_embedding_np = query_embedding.cpu().numpy().astype('float32')
            
            distances, indices = self.index.search(query_embedding_np, min(top_k, len(self.documents)))
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.documents):
                    results.append((self.documents[idx], float(distance)))
            return results
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return [(doc, 0.0) for doc in self.documents[:top_k]]

    def retrieve_by_category(self, query: str, category: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        """Retrieve documents filtered by category"""
        category_docs = self.kb.get_documents_by_category(category)
        if not category_docs:
            return []
        
        # Simple keyword matching for fallback
        results = []
        query_lower = query.lower()
        for doc in category_docs:
            if query_lower in doc.content.lower() or query_lower in doc.title.lower():
                results.append((doc, 0.0))
        
        return results[:top_k]


class RAGContext:
    """Builds context from retrieved documents"""

    @staticmethod
    def build_context(documents: List[Tuple[Document, float]], max_tokens: int = 1500) -> str:
        """Build context string from retrieved documents"""
        context_parts = []
        token_count = 0
        
        for doc, score in documents:
            doc_text = f"Source: {doc.source} ({doc.category})\nTitle: {doc.title}\n{doc.content}\n"
            tokens = len(doc_text.split())
            
            if token_count + tokens > max_tokens:
                break
            
            context_parts.append(doc_text)
            token_count += tokens
        
        return "\n---\n".join(context_parts)

    @staticmethod
    def format_response_with_sources(answer: str, documents: List[Tuple[Document, float]]) -> str:
        """Format response with source citations"""
        sources = set()
        for doc, _ in documents:
            sources.add(f"{doc.title} ({doc.source})")
        
        if sources:
            answer += "\n\nSources:\n"
            for source in sources:
                answer += f"• {source}\n"
        
        return answer
