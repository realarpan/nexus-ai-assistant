"""Core AI engine with LangChain and OpenAI integration"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any
import openai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIEngine:
    """Advanced AI engine for conversational AI"""
    
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        openai.api_key = self.openai_api_key
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            max_tokens=2000,
            openai_api_key=self.openai_api_key
        )
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=self.openai_api_key
        )
        
        # System prompt
        self.system_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are Nexus, an advanced AI assistant with expertise in various domains.
            You are helpful, creative, clever, and very friendly.
            
            Context: {context}
            
            Human: {question}
            
            Assistant: Let me help you with that."""
        )
    
    async def generate_response(
        self,
        message: str,
        context: List[Dict[str, str]] = None,
        user_preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate AI response to user message"""
        try:
            # Build conversation history
            messages = []
            if context:
                for msg in context[-5:]:  # Last 5 messages for context
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": message})
            
            # Generate response
            response = await self.llm.agenerate([messages])
            
            ai_message = response.generations[0][0].text
            tokens_used = response.llm_output.get("token_usage", {}).get("total_tokens", 0)
            
            return {
                "response": ai_message,
                "tokens_used": tokens_used,
                "model": "gpt-4-turbo-preview"
            }
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            raise
    
    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        try:
            embeddings = await self.embeddings.aembed_query(text)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    async def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Summarize long text"""
        try:
            prompt = f"Please provide a concise summary (max {max_length} words) of the following text:\n\n{text}"
            response = await self.llm.apredict(prompt)
            return response
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            raise

# Global AI engine instance
ai_engine = AIEngine()