import json
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Please add it to your .env file.")

    return genai.Client(api_key=api_key)


def rewrite_email_with_gemini(prompt: str, tone: str) -> dict:
    client = get_client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    raw_text = response.text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "rewritten_email": raw_text,
            "tone": tone,
            "key_changes": [
                "The model returned plain text instead of JSON."
            ],
        }