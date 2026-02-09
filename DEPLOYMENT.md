# Deployment Guide - Financial RAG Assistant

## Overview

This guide covers deploying the Financial RAG Assistant to production using:
- **Frontend**: Vercel
- **Backend Services**: Render
- **Vector DB**: Pinecone (managed)
- **LLM**: OpenAI (managed)

## Prerequisites

- GitHub repository with your code
- Vercel account (https://vercel.com)
- Render account (https://render.com)
- Pinecone account with production index
- OpenAI account with API key

## 1. Deploy Backend API (Go) to Render

### Step 1: Create New Web Service

1. Log in to Render
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `financial-rag-backend`
   - **Environment**: `Docker`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend-go`
   - **Docker Command**: (leave default)

### Step 2: Configure Environment Variables

Add the following environment variables:

```
GO_PORT=8080
GO_ENV=production
RAG_SERVICE_URL=https://your-rag-service.onrender.com
```

### Step 3: Deploy

Click "Create Web Service" and wait for deployment to complete.

Note the service URL (e.g., `https://financial-rag-backend.onrender.com`)

## 2. Deploy RAG Service (Python) to Render

### Step 1: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `financial-rag-service`
   - **Environment**: `Docker`
   - **Region**: Same as backend
   - **Branch**: `main`
   - **Root Directory**: `rag-service`
   - **Docker Command**: (leave default)

### Step 2: Configure Environment Variables

Add the following environment variables:

```
PYTHON_PORT=8000
PYTHON_ENV=production
PINECONE_API_KEY=your_production_pinecone_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=financial-docs
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
TOP_K=5
MAX_TOKENS=500
TEMPERATURE=0.7
```

### Step 3: Deploy

Click "Create Web Service" and wait for deployment.

Note the service URL (e.g., `https://financial-rag-service.onrender.com`)

### Step 4: Update Backend Environment

Go back to your backend service and update `RAG_SERVICE_URL` with the actual RAG service URL.

## 3. Deploy Frontend to Vercel

### Step 1: Import Project

1. Log in to Vercel
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 2: Configure Environment Variables

Add the following environment variable:

```
NEXT_PUBLIC_API_URL=https://financial-rag-backend.onrender.com
```

### Step 3: Deploy

Click "Deploy" and wait for deployment to complete.

Your frontend will be available at a Vercel URL (e.g., `https://your-app.vercel.app`)

## 4. Update CORS Configuration

After deployment, update the CORS settings in your backend:

Edit `backend-go/middleware/cors.go`:

```go
config.AllowOrigins = []string{
    "https://your-app.vercel.app",
    "https://*.vercel.app",
}
```

Commit and push changes to trigger redeployment.

## 5. Index Production Data

Before your application is fully functional, index your documents to the production Pinecone index:

```bash
# Set production environment variables
export PINECONE_API_KEY=your_production_key
export PINECONE_ENVIRONMENT=your_environment
export OPENAI_API_KEY=your_openai_key

# Run indexing script
cd scripts
python index_to_pinecone.py
```

## 6. Verify Deployment

### Health Checks

```bash
# Backend API
curl https://financial-rag-backend.onrender.com/health

# RAG Service
curl https://financial-rag-service.onrender.com/health
```

### End-to-End Test

1. Visit your Vercel frontend URL
2. Submit a test query
3. Verify you receive a proper response with sources

## Security Considerations

### 1. Environment Variables

- Never commit `.env` files
- Use platform-specific secret management
- Rotate API keys regularly

### 2. CORS

- Restrict to specific domains in production
- Remove wildcard origins

### 3. Rate Limiting

Consider adding rate limiting:
- Render: Use Render's built-in rate limiting
- Vercel: Use Vercel's Edge Config
- Application-level: Implement in Go backend

### 4. HTTPS

- All services should use HTTPS (automatic on Vercel and Render)
- Verify SSL certificates are valid

### 5. API Key Protection

- Never expose API keys in frontend code
- Use backend as proxy for all external API calls

## Monitoring

### Render

- View logs in Render dashboard
- Set up alerts for service downtime
- Monitor resource usage

### Vercel

- Use Vercel Analytics
- Monitor function execution time
- Track error rates

### Pinecone

- Monitor index usage and quota
- Track query performance
- Set up alerts for quota limits

## Cost Optimization

### Render

- Use free tier for development
- Scale to paid plans as needed
- Consider instance size based on traffic

### Vercel

- Free tier suitable for moderate traffic
- Monitor bandwidth usage
- Optimize image and asset delivery

### Pinecone

- Start with free tier (1 index, limited storage)
- Upgrade as data grows
- Monitor query volume

### OpenAI

- Use gpt-3.5-turbo for cost efficiency
- Implement caching for repeated queries
- Set max_tokens limits
- Monitor usage in OpenAI dashboard

## Troubleshooting

### Service Not Responding

1. Check Render/Vercel logs
2. Verify environment variables
3. Test health endpoints
4. Check service status pages

### CORS Errors

1. Verify allowed origins in backend
2. Check frontend is using correct API URL
3. Ensure credentials are properly configured

### Pinecone Connection Issues

1. Verify API key and environment
2. Check index exists and has data
3. Monitor Pinecone status page

### High Latency

1. Check service regions (should be close together)
2. Monitor Pinecone query performance
3. Optimize embedding generation
4. Consider caching strategies

## Rollback Procedure

### Render

- Use "Manual Deploy" to redeploy previous commit
- Or revert Git commit and push

### Vercel

- Go to Deployments tab
- Click "..." on previous deployment
- Select "Promote to Production"

## Continuous Deployment

Both Render and Vercel support automatic deployments:

1. Push to `main` branch triggers deployment
2. Pull requests create preview deployments
3. Configure branch protection rules
4. Set up CI/CD tests before deployment

## Custom Domain (Optional)

### Vercel

1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed

### Render

1. Go to Service Settings → Custom Domains
2. Add your domain
3. Update DNS records

Ensure both services use the same root domain for proper CORS configuration.
