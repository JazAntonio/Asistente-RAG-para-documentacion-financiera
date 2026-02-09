# Asistente RAG para Documentación Financiera

## 🎯 Descripción

Sistema inteligente de consulta de documentación financiera basado en **Retrieval-Augmented Generation (RAG)** que permite realizar preguntas en lenguaje natural y obtener respuestas precisas fundamentadas en documentos indexados.

## 🏗️ Arquitectura

El sistema implementa una arquitectura de microservicios moderna y escalable:

- **Frontend**: Next.js 14 con TypeScript y Tailwind CSS
- **Backend API**: Go con framework Gin (API Gateway)
- **Servicio RAG**: Python con FastAPI y LangChain
- **Base de Datos Vectorial**: Pinecone
- **Modelo de Lenguaje**: OpenAI (GPT-5 Nano / GPT-4o)

## ✨ Características

- ✅ Consultas en lenguaje natural
- ✅ Respuestas contextualizadas basadas en documentos
- ✅ Citación de fuentes utilizadas
- ✅ Interfaz web moderna y responsiva
- ✅ Arquitectura desacoplada y escalable
- ✅ Contenedorización con Docker
- ✅ Búsqueda semántica con embeddings
- ✅ Listo para producción (Vercel & Render)
- ✅ Validación de entrada y manejo de errores

## 🚀 Inicio Rápido

### Prerequisitos

- Docker y Docker Compose
- API keys de Pinecone y OpenAI
- Node.js 20+, Go 1.21+, Python 3.11+ (para desarrollo local)

### Configuración

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Financial_RAG
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus API keys
   ```

3. **Indexar documentos**
   ```bash
   cd scripts
   pip install -r requirements.txt
   python index_to_pinecone.py
   ```

4. **Iniciar servicios**
   ```bash
   docker-compose up --build
   ```

5. **Acceder a la aplicación**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8080
   - RAG Service: http://localhost:8000

## 🌐 Despliegue en la Nube

El sistema está optimizado para funcionar en entornos de producción modernos:

- **Frontend**: Diseñado para **Vercel** con soporte nativo para Next.js.
- **Backend (Go) & RAG Service (Python)**: Configurados para **Render** mediante Docker.
- **Infraestructura**: Utiliza servicios gestionados de **Pinecone** (Vector DB) y **OpenAI** (Modelos de IA).

Para más detalles, consulta la [**Guía de Despliegue**](DEPLOYMENT.md).

## 📚 Documentación

- [**SETUP.md**](SETUP.md) - Guía detallada de instalación y configuración
- [**DEPLOYMENT.md**](DEPLOYMENT.md) - Guía de despliegue a producción
- [**diagrams/architecture.md**](diagrams/architecture.md) - Diagramas de arquitectura

## 🗂️ Estructura del Proyecto

```
Financial_RAG/
├── frontend/              # Aplicación Next.js
│   ├── app/              # App Router de Next.js
│   ├── lib/              # Utilidades y clientes API
│   └── Dockerfile
├── backend-go/           # API Gateway en Go
│   ├── handlers/         # Manejadores de rutas
│   ├── clients/          # Clientes HTTP
│   ├── middleware/       # Middleware (CORS, etc.)
│   └── Dockerfile
├── rag-service/          # Servicio RAG en Python
│   ├── services/         # Lógica de negocio
│   ├── models/           # Modelos Pydantic
│   ├── config.py         # Configuración
│   └── Dockerfile
├── datasets/             # Documentos de ejemplo
├── scripts/              # Scripts de indexación
├── diagrams/             # Diagramas de arquitectura
└── docker-compose.yml    # Orquestación de servicios
```

## 🔐 Seguridad

- ✅ Validación de entrada con límites de longitud
- ✅ Variables de entorno para credenciales
- ✅ CORS configurado para orígenes específicos
- ✅ Contenedores con usuarios no-root
- ✅ HTTPS requerido en producción
- ✅ Sin exposición de API keys en el frontend

## 🛠️ Tecnologías

| Componente | Tecnología |
|-----------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Backend | Go 1.21, Gin Framework |
| RAG Service | Python 3.11, FastAPI, LangChain |
| Vector DB | Pinecone |
| LLM | OpenAI (GPT-5 Nano) |
| Embeddings | OpenAI (text-embedding-3-small) |
| Containerización | Docker, Docker Compose |
| Deployment | Vercel (Frontend), Render (Backend) |

## 📊 Flujo de Datos

1. Usuario ingresa pregunta en la interfaz web
2. Frontend envía consulta al Backend API (Go)
3. Backend valida y reenvía al Servicio RAG (Python)
4. RAG genera embedding de la consulta
5. Búsqueda semántica en Pinecone
6. Recuperación de documentos relevantes
7. Construcción de prompt con contexto
8. Generación de respuesta con LLM
9. Retorno de respuesta con fuentes citadas

## 🧪 Ejemplos de Consultas

- "¿Cuáles son los requisitos de capital para instituciones financieras?"
- "¿Qué políticas existen para la gestión de riesgo de liquidez?"
- "¿Cuáles son las normas de prevención de lavado de dinero?"
- "¿Qué requisitos hay para la divulgación financiera?"

## 📈 Escalabilidad

- Servicios independientes escalables horizontalmente
- Caching de embeddings para reducir costos
- Procesamiento asíncrono
- Pool de conexiones HTTP

## 🤝 Contribución

Este proyecto es una implementación técnica de referencia. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🔗 Enlaces Útiles

- [Documentación de Pinecone](https://docs.pinecone.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [LangChain Documentation](https://python.langchain.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Gin Framework](https://gin-gonic.com/)

## 💡 Notas

- El sistema utiliza documentación financiera sintética para demostración
- Los costos de API (OpenAI y Pinecone) son responsabilidad del usuario
- Se recomienda implementar rate limiting en producción
- Considerar caching para consultas frecuentes

---

**Desarrollado con ❤️ usando RAG, Next.js, Go y Python**
