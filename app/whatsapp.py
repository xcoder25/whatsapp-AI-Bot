import httpx
from .config import settings
from .ai import generate_reply

GRAPH_BASE = "https://graph.facebook.com/v20.0"

def graph_messages_url() -> str:
    return f"{GRAPH_BASE}/{settings.whatsapp_phone_number_id}/messages"

async def send_text_message(to: str, body: str) -> dict:
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body},
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(graph_messages_url(), headers=headers, json=payload)
        r.raise_for_status()
        return r.json()

async def handle_incoming_message(from_number: str, text_body: str):
    # Determine reply: AI or echo
    reply = await generate_reply(text_body)
    return await send_text_message(from_number, reply)
