from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
import os

load_dotenv()

class Settings(BaseModel):
    openai_api_key: str = Field(..., min_length = 1)
    openai_model: str = Field(..., min_length = 1)
    openai_embedding_model: str = Field(..., min_length = 1)

def load_settings() -> Settings: 
    try:
        return Settings(
                openai_api_key = os.getenv("OPENAI_API_KEY", ""),
                openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                openai_embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small",),

        )
    except ValidationError as e:
        raise RuntimeError(
            "Invalid configuration. Copy .env.example to .env and fill in the required values."
        ) from e

