from typing import Dict

from langchain_openai import AzureChatOpenAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from app.core.config import settings


_LLM_CACHE: Dict[str, object] = {}


def get_llm():
    """
    Centralized LLM factory with provider-only cache.
    """

    provider = settings.LLM_PROVIDER.lower()

    if provider in _LLM_CACHE:
        return _LLM_CACHE[provider]

  
    if provider == "nvidia":
        llm = ChatNVIDIA(
            model=settings.NVIDIA_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.NVIDIA_API_KEY,
            base_url=settings.NVIDIA_BASE_URL,
        )

  
    elif provider in ("azure", "azure_openai"):
        llm = AzureChatOpenAI(
            azure_deployment=settings.AZURE_DEPLOYMENT_NAME,
            api_version=settings.AZURE_API_VERSION,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.AZURE_API_KEY,
            model=settings.AZURE_MODEL,
            azure_endpoint=settings.AZURE_ENDPOINT,
        )
       

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    _LLM_CACHE[provider] = llm
    return llm