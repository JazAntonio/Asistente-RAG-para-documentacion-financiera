from typing import List, Dict, Any
from services.embeddings import EmbeddingService
from services.vector_store import VectorStoreService
from services.llm import LLMService
from models.schemas import QueryResponse, Source
from config import settings
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Complete RAG pipeline orchestration"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
        self.llm_service = LLMService()
        logger.info("RAG Pipeline initialized")
    
    def process_query(self, query: str) -> QueryResponse:
        """
        Process a user query through the complete RAG pipeline
        
        Args:
            query: User question
            
        Returns:
            QueryResponse with answer and sources
        """
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Step 1: Generate query embedding
            logger.debug("Generating query embedding...")
            query_embedding = self.embedding_service.generate_embedding(query)
            
            # Step 2: Retrieve relevant documents
            logger.debug("Retrieving relevant documents...")
            retrieved_docs = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=settings.top_k
            )
            
            if not retrieved_docs:
                logger.warning("No documents retrieved from vector store")
                return QueryResponse(
                    answer="Lo siento, no encontré información relevante para responder tu pregunta.",
                    sources=[]
                )
            
            # Step 3: Extract document texts for context
            context_texts = [doc["content"] for doc in retrieved_docs]
            
            # Step 4: Generate response using LLM
            logger.debug("Generating LLM response...")
            answer = self.llm_service.generate_response(
                query=query,
                context_documents=context_texts
            )
            
            # Step 5: Format sources
            sources = self._format_sources(retrieved_docs)
            
            logger.info("Query processing completed successfully")
            return QueryResponse(
                answer=answer,
                sources=sources
            )
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}", exc_info=True)
            raise
    
    def _format_sources(self, documents: List[Dict[str, Any]]) -> List[Source]:
        """Format retrieved documents as Source objects"""
        sources = []
        for doc in documents:
            source = Source(
                content=doc["content"],
                metadata={
                    "document_id": doc["id"],
                    "score": doc["score"],
                    **{k: v for k, v in doc["metadata"].items() if k != "text"}
                }
            )
            sources.append(source)
        return sources
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all pipeline components"""
        return {
            "vector_store": self.vector_store.health_check()
        }
