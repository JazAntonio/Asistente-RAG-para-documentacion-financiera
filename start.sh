#!/bin/bash

# Financial RAG Assistant - Quick Start Script

echo "🚀 Financial RAG Assistant - Quick Start"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your API keys before continuing"
    echo ""
    exit 1
fi

# Check for required environment variables
source .env

if [ -z "$PINECONE_API_KEY" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: API keys not configured in .env file"
    echo "Please set PINECONE_API_KEY and OPENAI_API_KEY"
    exit 1
fi

echo "✅ Environment variables configured"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Ask if user wants to index documents
read -p "Do you want to index sample documents to Pinecone? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Indexing documents to Pinecone..."
    cd scripts
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install -q -r requirements.txt
    python index_to_pinecone.py
    deactivate
    cd ..
    echo ""
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose up --build -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Access points:"
echo "   - Frontend:     http://localhost:3000"
echo "   - Backend API:  http://localhost:8080"
echo "   - RAG Service:  http://localhost:8000"
echo ""
echo "📝 View logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
echo ""
