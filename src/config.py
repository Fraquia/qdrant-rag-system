from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    llm_temperature: float = 0.7
    embedding_model: str = "text-embedding-3-large"
    cors_origins: list[str] = ["http://localhost", "http://localhost:3000"]
    api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
