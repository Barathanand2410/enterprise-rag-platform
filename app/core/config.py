from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise RAG Platform"
    APP_VERSION: str = "1.0.0"
    UPLOAD_DIR: str = "data/uploads"

    GOOGLE_API_KEY: str = ""
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    CHAT_MODEL: str = "gemini-1.5-flash"

    VECTOR_DB_DIR: str = "./chroma_storage"
    VECTOR_COLLECTION_NAME: str = "enterprise_rag_docs"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()