# Setup Guide - Financial RAG Assistant

## Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** 20+ and npm
- **Go** 1.21+
- **Python** 3.11+
- **Docker** and Docker Compose
- **Git**

## Required API Keys

You'll need accounts and API keys for:

1. **Pinecone** (https://www.pinecone.io/)
   - Create a free account
   - Create a new project
   - Get your API key and environment

2. **OpenAI** (https://platform.openai.com/)
   - Create an account
   - Generate an API key
   - Ensure you have credits available

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Financial_RAG
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Pinecone Configuration
PINECONE_API_KEY=your_actual_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=financial-docs

# OpenAI Configuration
OPENAI_API_KEY=your_actual_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Service URLs (for local development)
BACKEND_URL=http://localhost:8080
RAG_SERVICE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8080
```

### 3. Index Sample Documents

Before running the application, you need to index the sample documents into Pinecone:

```bash
cd scripts
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python index_to_pinecone.py
```

This will:
- Load sample financial documents
- Generate embeddings using OpenAI
- Create a Pinecone index
- Upload vectors to Pinecone

### 4. Run with Docker Compose (Recommended)

The easiest way to run all services:

```bash
# From project root
docker-compose up --build
```

This will start:
- Frontend on http://localhost:3000
- Backend API on http://localhost:8080
- RAG Service on http://localhost:8000

### 5. Run Services Individually (Alternative)

If you prefer to run services separately for development:

#### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Access at: http://localhost:3000

#### Backend API (Go)

```bash
cd backend-go
go mod download
go run main.go
```

Access at: http://localhost:8080

#### RAG Service (Python)

```bash
cd rag-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access at: http://localhost:8000

## Verification

### 1. Check Service Health

```bash
# Backend API
curl http://localhost:8080/health

# RAG Service
curl http://localhost:8000/health
```

### 2. Test Query

Open your browser and navigate to http://localhost:3000

Try a sample query:
```
¿Cuáles son los requisitos de capital para instituciones financieras?
```

You should receive a response based on the indexed documents.

## Troubleshooting

### Pinecone Connection Issues

- Verify your API key and environment are correct
- Check that the index was created successfully
- Ensure you have available quota in your Pinecone account

### OpenAI API Errors

- Verify your API key is valid
- Check you have available credits
- Ensure you're not hitting rate limits

### Docker Issues

- Ensure Docker daemon is running
- Try `docker-compose down` and rebuild with `docker-compose up --build`
- Check logs: `docker-compose logs <service-name>`

### Port Conflicts

If ports are already in use, you can modify them in:
- `docker-compose.yml` for Docker setup
- `.env` file for individual services

## Development Tips

1. **Hot Reload**: All services support hot reload in development mode
2. **Logs**: Check service logs for debugging
3. **Environment**: Keep `.env` file secure and never commit it
4. **Testing**: Test each service independently before integration

## Next Steps

- Review the [Architecture Documentation](diagrams/architecture.md)
- Check the [Deployment Guide](DEPLOYMENT.md) for production setup
- Explore the sample queries in the datasets folder
