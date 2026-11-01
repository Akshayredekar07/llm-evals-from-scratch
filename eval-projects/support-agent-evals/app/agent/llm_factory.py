import os
from functools import lru_cache

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_cerebras import ChatCerebras
from langchain_nebius import ChatNebius


SUPPORTED_PROVIDERS = {"nebius", "nvidia", "cerebras", "openrouter"}


def _require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(
            f"Missing required environment variable: {key}. "
            f"Add it to your .env file."
        )
    return value


def _get_nvidia_llm() -> BaseChatModel:
    if ChatNVIDIA is None:
        raise ImportError(
            "Install the NVIDIA integration: pip install langchain-nvidia-ai-endpoints"
        )

    return ChatNVIDIA(
        model=os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct"),
        api_key=_require_env("NVIDIA_API_KEY"),
        base_url=os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
        temperature=0,
        max_retries=2,
        timeout=60,
    )


def _get_cerebras_llm() -> BaseChatModel:
    if ChatCerebras is None:
        raise ImportError(
            "Install the Cerebras integration: pip install langchain-cerebras"
        )

    return ChatCerebras(
        model=os.getenv("CEREBRAS_MODEL", "llama-3.3-70b"),
        api_key=SecretStr(_require_env("CEREBRAS_API_KEY")),
        temperature=0,
        max_retries=2,
        timeout=60,
    )


def _get_nebius_llm() -> BaseChatModel:
    return ChatOpenAI(
        model=os.getenv("NEBIUS_MODEL", "MiniMaxAI/MiniMax-M3.1-Flash"),
        api_key=SecretStr(_require_env("NEBIUS_API_KEY")),
        base_url=os.getenv(
            "NEBIUS_BASE_URL",
            "https://api.tokenfactory.us-north1.nebius.com/v1/",
        ),
        temperature=0,
        max_retries=2,
        timeout=60,
    )


def _get_openrouter_llm() -> BaseChatModel:
    return ChatOpenAI(
        model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        api_key=SecretStr(_require_env("OPENROUTER_API_KEY")),
        base_url=os.getenv(
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1",
        ),
        temperature=0,
        max_retries=2,
        timeout=60,
    )


PROVIDER_FACTORIES = {
    "nebius": _get_nebius_llm,
    "nvidia": _get_nvidia_llm,
    "cerebras": _get_cerebras_llm,
    "openrouter": _get_openrouter_llm,
}


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    provider = os.getenv("MODEL_PROVIDER", "nebius").lower().strip()

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported MODEL_PROVIDER '{provider}'. "
            f"Supported providers: {', '.join(sorted(SUPPORTED_PROVIDERS))}"
        )

    return PROVIDER_FACTORIES[provider]()


def get_llm_for_provider(provider: str) -> BaseChatModel:
    provider = provider.lower().strip()

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported provider '{provider}'. "
            f"Supported providers: {', '.join(sorted(SUPPORTED_PROVIDERS))}"
        )

    return PROVIDER_FACTORIES[provider]()