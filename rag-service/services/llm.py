from typing import List
from openai import OpenAI
from config import settings
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with OpenAI language models"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        logger.info(f"Initialized LLMService with model: {self.model}")
    
    def generate_response(
        self,
        query: str,
        context_documents: List[str],
        max_tokens: int = None,
        temperature: float = None
    ) -> str:
        """
        Generate a response using the LLM with provided context
        
        Args:
            query: User query
            context_documents: List of relevant document excerpts
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Generated response text
        """
        try:
            # Use settings defaults if not provided
            max_tokens = max_tokens or settings.max_tokens
            temperature = temperature or settings.temperature
            
            # Build context from documents
            context = self._build_context(context_documents)
            
            # Create prompt
            prompt = self._create_prompt(query, context)
            
            # Prepare API parameters
            api_params = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en documentación financiera. "
                                   "Responde preguntas basándote ÚNICAMENTE en el contexto proporcionado. "
                                   "Si la información no está en el contexto, indica que no tienes suficiente información. "
                                   "Sé preciso, claro y profesional."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_completion_tokens": max_tokens,
            }
            
            # GPT-5 Nano only supports temperature=1 (default)
            # Only add temperature if it's not 1 and model is not gpt-5-nano
            if "gpt-5" not in self.model.lower() or temperature == 1:
                api_params["temperature"] = temperature
            else:
                logger.warning(f"Model {self.model} only supports temperature=1, ignoring temperature={temperature}")
            
            # Call OpenAI API
            response = self.client.chat.completions.create(**api_params)
            
            answer = response.choices[0].message.content.strip()
            logger.info(f"Generated response of length {len(answer)}")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise
    
    def _build_context(self, documents: List[str]) -> str:
        """Build context string from document list"""
        if not documents:
            return "No hay contexto disponible."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[Documento {i}]\n{doc}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create the final prompt with query and context"""
        prompt = f"""Contexto de documentos financieros:

{context}

Pregunta del usuario: {query}

Responde la pregunta basándote únicamente en el contexto proporcionado. Si la respuesta no se encuentra en el contexto, indícalo claramente."""
        
        return prompt
