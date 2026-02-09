from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import QueryRequest, QueryResponse, HealthResponse
from services.rag_pipeline import RAGPipeline
from config import settings
import logging
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Financial RAG Service",
    description="RAG microservice for financial documentation queries",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://backend-go:8080",
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline
try:
    rag_pipeline = RAGPipeline()
    logger.info("RAG pipeline initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG pipeline: {e}")
    rag_pipeline = None


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "service": "rag-service",
        "pinecone_connected": False
    }
    
    if rag_pipeline:
        try:
            component_health = rag_pipeline.health_check()
            health_status["pinecone_connected"] = component_health.get("vector_store", False)
        except Exception as e:
            logger.error(f"Health check error: {e}")
    
    return health_status


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process a user query through the RAG pipeline
    
    Args:
        request: QueryRequest with user query
        
    Returns:
        QueryResponse with answer and sources
    """
    if not rag_pipeline:
        raise HTTPException(
            status_code=503,
            detail="RAG service not initialized. Please check configuration."
        )
    
    try:
        logger.info(f"Received query: {request.query[:100]}...")
        response = rag_pipeline.process_query(request.query)
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Financial RAG Service",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.python_port,
        reload=settings.python_env == "development"
    )
