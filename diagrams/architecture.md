# Financial RAG Assistant - Architecture

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        User[User Browser]
    end
    
    subgraph "Frontend Layer"
        Next[Next.js Frontend<br/>Port 3000]
    end
    
    subgraph "API Gateway Layer"
        Go[Go Backend API<br/>Port 8080]
    end
    
    subgraph "AI/ML Layer"
        RAG[Python RAG Service<br/>Port 8000]
    end
    
    subgraph "External Services"
        Pinecone[(Pinecone<br/>Vector DB)]
        OpenAI[OpenAI API<br/>Embeddings + LLM]
    end
    
    User -->|HTTPS| Next
    Next -->|REST API| Go
    Go -->|HTTP| RAG
    RAG -->|Query Vectors| Pinecone
    RAG -->|Generate Response| OpenAI
    
    style Next fill:#0ea5e9
    style Go fill:#00add8
    style RAG fill:#3776ab
    style Pinecone fill:#000000,color:#fff
    style OpenAI fill:#10a37f
```

## Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend API
    participant R as RAG Service
    participant P as Pinecone
    participant L as OpenAI LLM
    
    U->>F: Submit Query
    F->>B: POST /api/query
    B->>R: POST /query
    
    R->>L: Generate Query Embedding
    L-->>R: Embedding Vector
    
    R->>P: Search Similar Vectors
    P-->>R: Top K Documents
    
    R->>L: Generate Response with Context
    L-->>R: Generated Answer
    
    R-->>B: Response + Sources
    B-->>F: JSON Response
    F-->>U: Display Answer & Sources
```

## Component Responsibilities

### Frontend (Next.js)
- **Technology**: Next.js 14, TypeScript, Tailwind CSS
- **Responsibilities**:
  - User interface for query input
  - Display responses and sources
  - Error handling and loading states
- **Port**: 3000

### Backend API (Go)
- **Technology**: Go 1.21, Gin framework
- **Responsibilities**:
  - API gateway and request routing
  - Input validation and sanitization
  - CORS and security headers
  - Rate limiting and timeout management
- **Port**: 8080

### RAG Service (Python)
- **Technology**: Python 3.11, FastAPI, LangChain
- **Responsibilities**:
  - Query embedding generation
  - Vector similarity search
  - Context retrieval from Pinecone
  - LLM prompt construction
  - Response generation
- **Port**: 8000

### Vector Database (Pinecone)
- **Type**: Managed cloud service
- **Responsibilities**:
  - Store document embeddings
  - Semantic similarity search
  - Metadata filtering

### LLM Provider (OpenAI)
- **Models**: 
  - Embeddings: text-embedding-ada-002
  - Generation: gpt-3.5-turbo or gpt-4
- **Responsibilities**:
  - Generate text embeddings
  - Generate contextual responses

## Security Considerations

1. **Input Validation**: Query length limits (max 1000 chars)
2. **CORS**: Restricted to known origins
3. **API Keys**: Stored in environment variables, never in code
4. **Docker**: Non-root users in containers
5. **HTTPS**: Required for production deployments
6. **Rate Limiting**: Implemented at API gateway level

## Scalability

- **Horizontal Scaling**: Each service can scale independently
- **Caching**: Embedding cache to reduce API calls
- **Async Processing**: Non-blocking I/O in all services
- **Connection Pooling**: Reuse HTTP connections

## Deployment Architecture

```mermaid
graph LR
    subgraph "Vercel"
        FE[Frontend]
    end
    
    subgraph "Render"
        BE[Backend API]
        RS[RAG Service]
    end
    
    subgraph "External"
        PC[Pinecone]
        OAI[OpenAI]
    end
    
    FE --> BE
    BE --> RS
    RS --> PC
    RS --> OAI
```
