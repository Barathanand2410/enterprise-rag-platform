from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


class LLMService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in .env")

        self.llm = ChatGoogleGenerativeAI(
            model=settings.CHAT_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

    def get_model(self):
        return self.llm

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)