#!/usr/bin/env python3
"""
Script to index financial documents into Pinecone vector database.
This script loads documents, generates embeddings, and uploads them to Pinecone.
"""

import json
import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "financial-docs")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSION = 1536  # Dimension for text-embedding-3-small and ada-002

# Validate configuration
if not all([PINECONE_API_KEY, PINECONE_CLOUD, PINECONE_REGION, OPENAI_API_KEY]):
    print("Error: Missing required environment variables")
    print("Please ensure PINECONE_API_KEY, PINECONE_CLOUD, PINECONE_REGION, and OPENAI_API_KEY are set")
    sys.exit(1)


def load_documents(file_path: str) -> List[Dict[str, Any]]:
    """Load documents from JSON file"""
    print(f"Loading documents from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    print(f"Loaded {len(documents)} documents")
    return documents


def generate_embeddings(texts: List[str], client: OpenAI) -> List[List[float]]:
    """Generate embeddings for a list of texts"""
    print(f"Generating embeddings for {len(texts)} texts...")
    
    embeddings = []
    batch_size = 100  # Process in batches to avoid rate limits
    
    for i in tqdm(range(0, len(texts), batch_size), desc="Generating embeddings"):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            input=batch,
            model=EMBEDDING_MODEL
        )
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)
    
    return embeddings


def create_pinecone_index(pc: Pinecone, index_name: str):
    """Create Pinecone index if it doesn't exist"""
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if index_name in existing_indexes:
        print(f"Index '{index_name}' already exists")
        return
    
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud=PINECONE_CLOUD,
            region=PINECONE_REGION
        )
    )
    print(f"Index '{index_name}' created successfully")


def index_documents(documents: List[Dict[str, Any]]):
    """Main function to index documents into Pinecone"""
    
    # Initialize clients
    print("Initializing OpenAI client...")
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    
    print("Initializing Pinecone client...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Create index if needed
    create_pinecone_index(pc, PINECONE_INDEX_NAME)
    
    # Connect to index
    index = pc.Index(PINECONE_INDEX_NAME)
    
    # Prepare texts for embedding
    texts = [doc["content"] for doc in documents]
    
    # Generate embeddings
    embeddings = generate_embeddings(texts, openai_client)
    
    # Prepare vectors for upload
    print("Preparing vectors for upload...")
    vectors = []
    for doc, embedding in zip(documents, embeddings):
        vector = {
            "id": doc["id"],
            "values": embedding,
            "metadata": {
                "text": doc["content"],
                "title": doc.get("title", ""),
                "category": doc.get("category", ""),
            }
        }
        vectors.append(vector)
    
    # Upload to Pinecone
    print(f"Uploading {len(vectors)} vectors to Pinecone...")
    batch_size = 100
    for i in tqdm(range(0, len(vectors), batch_size), desc="Uploading vectors"):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
    
    print("✅ Indexing completed successfully!")
    
    # Verify upload
    stats = index.describe_index_stats()
    print(f"Index stats: {stats}")


def main():
    """Main entry point"""
    # Path to documents
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    docs_path = os.path.join(project_root, "datasets", "sample_financial_docs.json")
    
    if not os.path.exists(docs_path):
        print(f"Error: Document file not found at {docs_path}")
        sys.exit(1)
    
    # Load and index documents
    documents = load_documents(docs_path)
    index_documents(documents)


if __name__ == "__main__":
    main()
