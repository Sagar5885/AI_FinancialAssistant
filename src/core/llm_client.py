"""
LLM client wrapper supporting multiple providers
"""
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)
import time

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        pass

    @abstractmethod
    def generate_with_context(self, prompt: str, context: str, **kwargs) -> str:
        """Generate response with context"""
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini LLM Provider"""

    def __init__(self, api_key: str, model: str = None, temperature: float = 0.7):
        try:
            import google.generativeai as genai
            self.genai = genai
            self.genai.configure(api_key=api_key)
            
            # If no model specified, try to use the latest available
            if not model:
                model = "gemini-1.5-flash"
            
            self.model = model
            self.temperature = temperature
            logger.info(f"Initialized Gemini provider with model: {self.model}")
        except ImportError:
            raise ImportError(
                "google-generativeai package required for Gemini provider"
            )

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Gemini with improved error handling"""
        max_retries = 3
        retry_count = 0
        last_error = None
        
        # Try different model names
        model_names = [
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro",  # Fallback for older API
        ]
        
        for model_name in model_names:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    logger.info(f"Trying model: {model_name}")
                    model = self.genai.GenerativeModel(model_name)
                    response = model.generate_content(
                        prompt,
                        generation_config=(
                            self.genai.types.GenerationConfig(
                                temperature=self.temperature,
                                max_output_tokens=kwargs.get(
                                    'max_tokens', 2000
                                ),
                            )
                        ),
                        request_options={"timeout": 30}
                    )
                    
                    if (response and hasattr(response, 'text') and
                            response.text):
                        logger.info(
                            f"Response from {model_name}"
                        )
                        return response.text
                    else:
                        logger.warning("Empty response, retrying...")
                        last_error = "Empty response"
                        retry_count += 1
                        time.sleep(2 ** retry_count)
                        continue
                        
                except Exception as e:
                    error_str = str(e).lower()
                    logger.warning(
                        f"{model_name} error: {e}"
                    )
                    last_error = e
                    retry_count += 1
                    
                    # If model not found, try next one
                    if "not found" in error_str or "404" in error_str:
                        logger.info(f"Model {model_name} not available")
                        break
                    
                    if any(x in error_str for x in [
                        'quota', 'rate', 'limit', '429', '503'
                    ]):
                        wait_time = min(10, 2 ** retry_count)
                        logger.info(f"Rate limited, waiting...")
                        time.sleep(wait_time)
                    elif retry_count < max_retries:
                        time.sleep(2 ** retry_count)
        
        # If all retries failed, raise error
        error_msg = f"All models failed: {last_error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    def generate_with_context(self, prompt: str, context: str, **kwargs) -> str:
        """Generate response with context"""
        full_prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}"
        return self.generate(full_prompt, **kwargs)


class OpenAIProvider(LLMProvider):
    """OpenAI GPT LLM Provider"""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = model
            self.temperature = temperature
            logger.info(f"Initialized OpenAI provider with model: {model}")
        except ImportError:
            raise ImportError("openai package required for OpenAI provider")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=kwargs.get('max_tokens', 2000),
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating with OpenAI: {str(e)}")
            raise

    def generate_with_context(self, prompt: str, context: str, **kwargs) -> str:
        """Generate response with context"""
        full_prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}"
        return self.generate(full_prompt, **kwargs)


class LLMClient:
    """Unified LLM client supporting multiple providers"""

    def __init__(self, provider: str = "gemini", api_key: Optional[str] = None, **kwargs):
        if provider.lower() == "gemini":
            self.provider = GeminiProvider(api_key or "", **kwargs)
        elif provider.lower() == "openai":
            self.provider = OpenAIProvider(api_key or "", **kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response"""
        return self.provider.generate(prompt, **kwargs)

    def generate_with_context(self, prompt: str, context: str, **kwargs) -> str:
        """Generate response with context"""
        return self.provider.generate_with_context(prompt, context, **kwargs)
