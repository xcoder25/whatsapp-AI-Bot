import os
from typing import Optional
from pathlib import Path

USE_AI = os.getenv("USE_AI", "false").lower() in ("1","true","yes")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

SYSTEM_PROMPT_PATH = Path("prompts/assistant.txt")

def load_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    # default prompt
    return (
        "You are ArukBot, the official AI assistant for Aruk Beauty Line.\n"
        "- Be polite, concise, and professional.\n"
        "- Answer only about skincare products, orders, shipping, and policies.\n"
        "- If unsure, ask to escalate to a human agent.\n"
        "- Keep replies under 120 words."
    )

async def generate_reply(user_text: str) -> str:
    """Generate a reply using Gemini (google-genai). Returns AI text or fallback echo."""
    if not USE_AI or not GEMINI_API_KEY:
        # fallback simple echo
        return f"You said: {user_text}"

    try:
        # Lazy import so project still runs if google-genai isn't installed
        from google import genai
        # Initialize client
        client = genai.Client(api_key=GEMINI_API_KEY)
        system_prompt = load_system_prompt()

        # Prepare prompt: system + user
        prompt = system_prompt + "\n\nUser: " + user_text

        # Call the text generation API. Using `models.generate` per google-genai docs.
        response = client.generate_text(model="gemini-1.5", input=prompt, max_output_tokens=512)
        # If structure differs, handle gracefully
        if hasattr(response, 'text'):
            return response.text.strip()
        # Otherwise, try dict-like access
        text = getattr(response, 'output', None) or response
        if isinstance(text, dict):
            # attempt common keys
            for k in ("text", "output", "content"):
                if k in text:
                    return text[k]
            # fallback to string conversion
            return str(text)
        return str(text).strip()
    except Exception as e:
        # On error, fallback to safe echo (do not crash webhook)
        print("Gemini error:", e)
        return f"(AI error) You said: {user_text}"
