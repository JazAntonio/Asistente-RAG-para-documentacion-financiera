from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Service for interacting with Pinecone vector database"""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name
        self.index = None
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize or connect to Pinecone index"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            
            if self.index_name not in [idx.name for idx in existing_indexes]:
                logger.warning(f"Index '{self.index_name}' does not exist")
                logger.info("Index will need to be created using the indexing script")
            else:
                self.index = self.pc.Index(self.index_name)
                logger.info(f"Connected to Pinecone index: {self.index_name}")
                
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            raise
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Pinecone
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of matching documents with metadata
        """
        if not self.index:
            raise RuntimeError("Pinecone index not initialized. Please run the indexing script first.")
        
        try:
            # Perform search
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            
            # Format results
            documents = []
            for match in results.matches:
                doc = {
                    "id": match.id,
                    "score": match.score,
                    "content": match.metadata.get("text", ""),
                    "metadata": match.metadata
                }
                documents.append(doc)
            
            logger.info(f"Retrieved {len(documents)} documents from Pinecone")
            return documents
            
        except Exception as e:
            logger.error(f"Error searching Pinecone: {e}")
            raise
    
    def health_check(self) -> bool:
        """Check if Pinecone connection is healthy"""
        try:
            if not self.index:
                return False
            
            # Try to get index stats
            stats = self.index.describe_index_stats()
            logger.debug(f"Pinecone index stats: {stats}")
            return True
            
        except Exception as e:
            logger.error(f"Pinecone health check failed: {e}")
            return False
