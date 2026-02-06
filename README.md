# Asistente RAG para Documentación Financiera

## 1. Descripción general

Este proyecto implementa un **asistente inteligente basado en Retrieval-Augmented Generation (RAG)** que permite consultar documentación financiera simulada mediante lenguaje natural. El sistema está diseñado como una solución técnica con una arquitectura moderna, desacoplada y orientada a producción.

El objetivo principal es:

- Diseñar una arquitectura de IA aplicada a consulta documental
- Integrar modelos de lenguaje con bases de datos vectoriales
- Implementar un flujo completo de ingestión, recuperación y generación
- Garantizar mantenibilidad, escalabilidad y control de costos

---

## 2. Funcionalidad principal

El sistema permite que un usuario:

1. Ingrese una pregunta en lenguaje natural desde una interfaz web.
2. El sistema recupere fragmentos relevantes de documentación financiera previamente indexada.
3. Un modelo de lenguaje genere una respuesta fundamentada exclusivamente en dichos documentos.
4. La respuesta sea presentada de forma clara en la interfaz.

El asistente evita respuestas genéricas y se apoya explícitamente en el contexto recuperado, lo que mejora la precisión y la trazabilidad de las respuestas.

---

## 3. Arquitectura general

La solución sigue una arquitectura distribuida basada en servicios independientes:

- **Frontend**: Aplicación web en Next.js
- **Backend API**: Servicio HTTP en Go
- **Servicio de IA (RAG)**: Microservicio en Python
- **Base de datos vectorial**: Pinecone
- **Modelos de lenguaje**: APIs externas (OpenAI, Anthropic o equivalentes)

Cada componente tiene responsabilidades bien definidas, lo que facilita el despliegue independiente, las pruebas y el mantenimiento.

---

## 4. Estructura del repositorio

El proyecto se organiza como un **monorepo**, con separación clara por dominio funcional:

```
rag-finance-assistant/
│
├── frontend/          # Aplicación Next.js
├── backend-go/        # API Gateway en Go
├── rag-service/       # Servicio RAG en Python
├── datasets/          # Documentos sintéticos o públicos
├── scripts/           # Scripts de ingesta y embeddings
├── docker-compose.yml # Orquestación local
├── README.md          # Documentación principal
└── diagrams/          # Diagramas de arquitectura
```

Esta estructura permite desarrollar y mantener todo el sistema desde un único repositorio y un solo IDE.

---

## 5. Frontend (Next.js)

El frontend está desarrollado en **Next.js** y se encarga exclusivamente de la interacción con el usuario.

Responsabilidades:

- Interfaz de consulta
- Envío de preguntas al backend
- Renderizado de respuestas

Tecnologías clave:

- Next.js (App Router)
- Fetch API
- Renderizado del lado del cliente

El frontend no contiene lógica de IA ni credenciales sensibles.

---

## 6. Backend API (Go)

El backend es una **aplicación HTTP escrita en Go**, desplegada como contenedor Docker.

Responsabilidades:

- Exponer endpoints públicos (por ejemplo, `/query`)
- Validar solicitudes y manejar errores
- Gestionar CORS, timeouts y control básico de tráfico
- Orquestar llamadas al servicio RAG

Tecnologías clave:

- Go (net/http o Gin)
- Docker para empaquetado

Go se utiliza por su rendimiento, manejo de concurrencia y estabilidad como capa de servicios.

---

## 7. Servicio RAG (Python)

El núcleo de la lógica de inteligencia artificial reside en un **microservicio independiente en Python**.

Responsabilidades:

- Generar embeddings de consultas
- Consultar la base de datos vectorial
- Construir prompts con contexto recuperado
- Llamar a modelos de lenguaje
- Retornar respuestas estructuradas

Tecnologías clave:

- Python 3.11
- LangChain / Hugging Face
- SDK de Pinecone
- APIs de LLM

Python se utiliza por su ecosistema dominante en IA y aprendizaje automático.

---

## 8. Base de datos vectorial (Pinecone)

Pinecone se utiliza como **almacén vectorial** para los embeddings de documentos.

Características:

- Servicio completamente gestionado
- Búsqueda semántica eficiente
- Uso de índices con metadatos

Los documentos se fragmentan, se transforman en embeddings y se indexan para su posterior recuperación semántica.

---

## 9. Dataset

El proyecto utiliza documentación financiera **no sensible**, obtenida de dos formas:

1. **Datos sintéticos**: Documentos ficticios generados con estructura y lenguaje técnico realista.
2. **Datos públicos**: Documentación abierta de organismos financieros internacionales.

Esto permite validar el pipeline completo de ingestión sin riesgos legales o de privacidad.

---

## 10. Contenedores y desarrollo local

Docker se utiliza para:

- Definir entornos reproducibles
- Ejecutar servicios de forma aislada
- Alinear el entorno local con el entorno de despliegue

Con `docker-compose` es posible levantar todo el sistema localmente para pruebas y desarrollo.

---

## 11. Despliegue

- **Frontend**: Vercel
- **Backend Go**: Render (Docker)
- **Servicio RAG**: Render (Docker)
- **Vector DB y LLMs**: Servicios externos

Las credenciales y configuraciones sensibles se gestionan mediante variables de entorno.

---

## 12. Alcance del proyecto

El sistema implementa un flujo RAG completo y funcional, enfocado en:

- Consulta semántica de documentos
- Integración robusta entre servicios
- Buenas prácticas de arquitectura e infraestructura

No está orientado a uso comercial directo, sino a servir como una implementación técnica clara, extensible y mantenible.

---

## 13. Tecnologías resumidas

- **Frontend**: Next.js
- **Backend**: Go
- **IA / RAG**: Python, LangChain
- **Vector DB**: Pinecone
- **Infraestructura**: Docker, Render, Vercel
- **IDE recomendado**: VS Code

