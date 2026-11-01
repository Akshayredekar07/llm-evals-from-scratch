import os

from dotenv import load_dotenv
from deepeval.models import OpenAIModel

load_dotenv()


def get_nebius_eval_model() -> OpenAIModel:
    return OpenAIModel(
        model=os.getenv(
            "NEBIUS_MODEL",
            "MiniMaxAI/MiniMax-M3.1-Flash",
        ),
        api_key=os.getenv("NEBIUS_API_KEY"),
        base_url=os.getenv(
            "NEBIUS_BASE_URL",
            "https://api.tokenfactory.us-north1.nebius.com/v1/",
        ),
        temperature=0,
    )