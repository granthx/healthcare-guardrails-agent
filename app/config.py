import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    use_mock_llm: bool = os.getenv(
        "USE_MOCK_LLM",
        "true" if not (os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")) else "false",
    ).lower() == "true"


settings = Settings()
