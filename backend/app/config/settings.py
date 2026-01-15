import os

class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instan")

settings = Settings()
