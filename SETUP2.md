# SETUP2.md - Financial RAG Assistant

## 📚 Guía Completa de Configuración

Esta guía cubre tanto el **desarrollo local** como el **despliegue en producción** del asistente RAG financiero.

---

## 📋 Tabla de Contenidos

1. [Prerequisitos](#-prerequisitos)
2. [Setup Local con Docker](#-setup-local-con-docker)
3. [Setup Local sin Docker](#-setup-local-sin-docker)
4. [Despliegue en Producción](#-despliegue-en-producción)
5. [Solución de Problemas](#-solución-de-problemas)
6. [FAQs](#-faqs)

---

## 🔧 Prerequisitos

### Para Desarrollo Local

#### Opción 1: Con Docker (Recomendado)
- **Docker Desktop** (versión 20.10+)
- **Docker Compose** (versión 2.0+)
- **Git**
- Claves de API:
  - OpenAI API Key
  - Pinecone API Key

#### Opción 2: Sin Docker
- **Node.js** (versión 18+) y **npm**
- **Go** (versión 1.21+)
- **Python** (versión 3.11+)
- **Git**
- Claves de API (igual que arriba)

### Para Despliegue en Producción

- **Cuentas necesarias**:
  - [Vercel](https://vercel.com) - Para el frontend
  - [Render](https://render.com) - Para backend y RAG service
  - [Pinecone](https://pinecone.io) - Vector database
  - [OpenAI](https://platform.openai.com) - LLM y embeddings
- **Repositorio Git** en GitHub (público o privado)

---

## 🐳 Setup Local con Docker

### Paso 1: Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd Financial_RAG
```

### Paso 2: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus claves
nano .env  # o usa tu editor preferido
```

**Variables mínimas requeridas:**

```bash
# Pinecone
PINECONE_API_KEY=tu_api_key_aqui
PINECONE_INDEX_NAME=financial-docs

# OpenAI
OPENAI_API_KEY=tu_api_key_aqui
OPENAI_MODEL=gpt-5-nano
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

### Paso 3: Crear Índice en Pinecone

1. Ve a [Pinecone Console](https://app.pinecone.io)
2. Crea un nuevo índice:
   - **Nombre**: `financial-docs`
   - **Dimensiones**: `1536`
   - **Metric**: `cosine`
   - **Cloud**: `AWS`
   - **Region**: `us-east-1`

### Paso 4: Indexar Documentos

```bash
# Activar entorno virtual de Python
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r rag-service/requirements.txt

# Ejecutar script de indexación
cd scripts
python index_to_pinecone.py
cd ..
```

### Paso 5: Iniciar la Aplicación

```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# O en modo background
docker-compose up -d --build
```

### Paso 6: Verificar que Todo Funciona

Abre tu navegador y visita:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080/health
- **RAG Service**: http://localhost:8000/health

### Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f frontend
docker-compose logs -f backend-go
docker-compose logs -f rag-service

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir un servicio específico
docker-compose up -d --build frontend
```

---

## 💻 Setup Local sin Docker

### Paso 1: Configurar RAG Service (Python)

```bash
cd rag-service

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Volver a la raíz
cd ..
```

### Paso 2: Configurar Backend (Go)

```bash
cd backend-go

# Descargar dependencias
go mod download

# Volver a la raíz
cd ..
```

### Paso 3: Configurar Frontend (Next.js)

```bash
cd frontend

# Instalar dependencias
npm install

# Volver a la raíz
cd ..
```

### Paso 4: Configurar Variables de Entorno

Igual que en el setup con Docker (ver arriba).

### Paso 5: Indexar Documentos

```bash
cd scripts
python index_to_pinecone.py
cd ..
```

### Paso 6: Iniciar Servicios

Necesitarás **3 terminales** separadas:

**Terminal 1 - RAG Service:**
```bash
cd rag-service
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Backend API:**
```bash
cd backend-go
go run main.go
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Paso 7: Verificar

Visita las mismas URLs que en el setup con Docker.

---

## 🚀 Despliegue en Producción

### Arquitectura de Despliegue

```
┌─────────────────┐
│  Usuario Final  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vercel         │  Frontend (Next.js)
│  Edge Network   │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  Render         │  Backend API (Go)
│  Web Service    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Render         │  RAG Service (Python)
│  Web Service    │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌─────────┐
│ Pinecone│ │ OpenAI  │
│ Vector  │ │   API   │
│   DB    │ │         │
└─────────┘ └─────────┘
```

### Método 1: Despliegue con Render Blueprint (Recomendado)

Este método usa el archivo `render.yaml` para desplegar ambos servicios backend con un solo click.

#### 1. Preparar Pinecone

1. Ve a [Pinecone Console](https://app.pinecone.io)
2. Crea un índice de **producción**:
   - **Nombre**: `financial-docs`
   - **Dimensiones**: `1536`
   - **Metric**: `cosine`
3. Indexa tus documentos apuntando al índice de producción

#### 2. Desplegar en Render usando Blueprint

1. Haz push de tu código a GitHub
2. Ve a [Render Dashboard](https://dashboard.render.com)
3. Click en **"New"** → **"Blueprint"**
4. Conecta tu repositorio de GitHub
5. Render detectará automáticamente el archivo `render.yaml`
6. **Configura las variables secretas** (las que tienen `sync: false`):
   - `PINECONE_API_KEY`: Tu API key de Pinecone
   - `OPENAI_API_KEY`: Tu API key de OpenAI
   - `ALLOWED_ORIGINS`: Déjalo vacío por ahora
7. Click en **"Apply"**
8. Espera a que ambos servicios se desplieguen
9. **Copia las URLs** de ambos servicios:
   - RAG Service: `https://financial-rag-service.onrender.com`
   - Backend: `https://financial-rag-backend.onrender.com`

#### 3. Desplegar Frontend en Vercel

1. Ve a [Vercel Dashboard](https://vercel.com/dashboard)
2. Click en **"Add New..."** → **"Project"**
3. Importa tu repositorio de GitHub
4. Configura el proyecto:
   - **Framework Preset**: Next.js (auto-detectado)
   - **Root Directory**: `frontend`
   - Vercel detectará automáticamente `vercel.json`
5. Agrega la variable de entorno:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://financial-rag-backend.onrender.com` (tu URL de Render)
6. Click en **"Deploy"**
7. Espera a que el despliegue termine
8. **Copia la URL** de Vercel: `https://tu-app.vercel.app`

#### 4. Configurar CORS

Ahora que tienes la URL de Vercel, actualiza el backend:

1. Ve a Render Dashboard → `financial-rag-backend` → Environment
2. Agrega/actualiza la variable:
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `https://tu-app.vercel.app`
3. Guarda y espera a que el servicio se redespliege automáticamente

#### 5. Verificar Despliegue

```bash
# Verificar health checks
curl https://financial-rag-service.onrender.com/health
curl https://financial-rag-backend.onrender.com/health

# Visitar frontend
# Abre https://tu-app.vercel.app en tu navegador
# Haz una consulta de prueba
```

### Método 2: Despliegue Manual (Sin Blueprint)

Si prefieres desplegar manualmente, sigue la guía completa en [`DEPLOYMENT.md`](DEPLOYMENT.md).

---

## 🔄 Actualizaciones y Redepliegues

### Desarrollo Continuo

**Render y Vercel** tienen **despliegue automático** habilitado por defecto:

```bash
# Hacer cambios en tu código
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main

# Render y Vercel redesplegarán automáticamente
```

### Preview Deployments (Vercel)

Para probar cambios antes de producción:

```bash
# Crear un branch de feature
git checkout -b feature/nueva-caracteristica

# Hacer cambios y push
git push origin feature/nueva-caracteristica

# Vercel creará automáticamente un preview deployment
# Recibirás una URL única para probar
```

---

## 🆘 Solución de Problemas

### Problema: "CORS Error" en el Frontend

**Síntomas:** Error en la consola del navegador sobre CORS.

**Solución:**
1. Verifica que `ALLOWED_ORIGINS` en Render incluya tu URL de Vercel
2. Asegúrate de incluir `https://` (no `http://`)
3. Espera a que el backend se redespliege después de cambiar la variable

### Problema: "Service Unavailable" en Render (Free Tier)

**Síntomas:** Primer request después de inactividad tarda mucho.

**Causa:** Los servicios gratuitos de Render se "duermen" después de 15 minutos.

**Soluciones:**
- Espera 30-60 segundos en el primer request
- Upgrade a plan pagado ($7/mes por servicio)
- Usa un servicio de "keep-alive" para hacer ping cada 10 minutos

### Problema: "Module not found" en Next.js

**Síntomas:** Error de build en Vercel sobre módulos faltantes.

**Solución:**
```bash
# Asegúrate de que package-lock.json esté en el repo
cd frontend
npm install
git add package-lock.json
git commit -m "chore: update package-lock.json"
git push
```

### Problema: Variables de Entorno no se Aplican

**Síntomas:** La aplicación usa valores por defecto en vez de tus variables.

**Solución:**
1. **Vercel**: Las variables deben empezar con `NEXT_PUBLIC_` para ser accesibles en el cliente
2. **Render**: Después de agregar variables, el servicio debe redeployarse
3. Verifica que no haya espacios extra en los valores

### Problema: "Error connecting to Pinecone"

**Síntomas:** RAG service falla al iniciar.

**Solución:**
1. Verifica que el índice existe en Pinecone
2. Verifica que `PINECONE_INDEX_NAME` coincida exactamente
3. Verifica que `PINECONE_API_KEY` sea válida
4. Revisa que la región sea correcta

### Problema: Docker se queda sin memoria

**Síntomas:** `docker-compose` falla con errores de memoria.

**Solución:**
```bash
# Aumentar memoria de Docker Desktop
# Settings → Resources → Memory → 4GB o más

# Limpiar recursos viejos
docker system prune -a
```

---

## ❓ FAQs

### ¿Puedo usar otro modelo de OpenAI?

Sí, cambia la variable `OPENAI_MODEL` en `.env`:

```bash
# Opciones disponibles:
OPENAI_MODEL=gpt-5-nano        # Más rápido, solo temperature=1
OPENAI_MODEL=gpt-4o            # Más potente
OPENAI_MODEL=gpt-4-turbo       # Balance
OPENAI_MODEL=gpt-3.5-turbo     # Más económico
```

> **Nota:** GPT-5 Nano solo soporta `TEMPERATURE=1`

### ¿Cuánto cuesta ejecutar esto en producción?

**Costos estimados mensuales:**

| Servicio | Free Tier | Producción |
|----------|-----------|------------|
| Vercel | 100GB bandwidth | $20/mes (Pro) |
| Render Backend | Gratis* | $7/mes |
| Render RAG | Gratis* | $7/mes |
| Pinecone | 1 índice, 100K vectors | $70/mes |
| OpenAI | Pay-per-use | ~$10-50/mes** |

\* Con cold starts  
\** Depende del uso

**Total mínimo:** $0/mes  
**Total recomendado:** ~$100-150/mes

### ¿Puedo usar otro vector database en vez de Pinecone?

Sí, pero necesitarás modificar `rag-service/services/vector_store.py` para usar otro cliente (Weaviate, Qdrant, ChromaDB, etc.).

### ¿Cómo agrego más documentos después del despliegue?

```bash
# Localmente, apuntando a Pinecone de producción
export PINECONE_API_KEY=tu_prod_key
cd scripts
python index_to_pinecone.py

# Los documentos estarán disponibles inmediatamente
```

### ¿Puedo usar un dominio personalizado?

**Vercel:**
1. Settings → Domains → Add Domain
2. Configura DNS según instrucciones
3. Actualiza `ALLOWED_ORIGINS` en Render con el nuevo dominio

**Render:**
1. Service Settings → Custom Domain
2. Configura DNS
3. Actualiza `NEXT_PUBLIC_API_URL` en Vercel

### ¿Cómo veo los logs en producción?

**Vercel:**
- Dashboard → Proyecto → Logs
- Real-time logs durante el build

**Render:**
- Dashboard → Service → Logs
- Logs en tiempo real y históricos

### ¿El proyecto soporta múltiples idiomas?

El sistema responde en el idioma de la pregunta. Puedes hacer preguntas en español, inglés, u otros idiomas y obtendrás respuestas coherentes.

### ¿Cómo mejoro la calidad de las respuestas?

1. **Mejores embeddings**: Usa `text-embedding-3-large` (más caro pero mejor)
2. **Más contexto**: Aumenta `TOP_K` de 5 a 7-10
3. **Modelo más potente**: Usa `gpt-4o` en vez de `gpt-3.5-turbo`
4. **Chunks más grandes**: Aumenta `CHUNK_SIZE` de 1000 a 1500
5. **Mejores documentos**: Asegúrate de que tus PDFs sean de calidad

---

## 📚 Recursos Adicionales

- [Documentación de Next.js](https://nextjs.org/docs)
- [Documentación de Gin (Go)](https://gin-gonic.com/docs/)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Pinecone](https://docs.pinecone.io/)
- [Documentación de OpenAI](https://platform.openai.com/docs)
- [`DEPLOYMENT.md`](DEPLOYMENT.md) - Guía detallada de despliegue
- [`README.md`](README.md) - Overview del proyecto

---

## 🤝 Soporte

Si encuentras problemas no cubiertos en esta guía:

1. Revisa los logs detallados de cada servicio
2. Verifica que todas las variables de entorno estén correctamente configuradas
3. Consulta la documentación de las plataformas específicas
4. Revisa los issues del repositorio

---

**¡Listo!** Tu asistente RAG financiero debería estar funcionando tanto localmente como en producción. 🎉
