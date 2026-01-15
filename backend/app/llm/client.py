import os
from groq import Groq
from backend.app.config.settings import settings

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2 )
    return response.choices[0].message.content
