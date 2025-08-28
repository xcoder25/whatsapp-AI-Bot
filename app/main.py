from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from .config import settings
from .security import verify_x_hub_signature_256
from .schemas import SendTextRequest
from .whatsapp import send_text_message, handle_incoming_message

app = FastAPI(title="WhatsApp Business Bot (Gemini-enabled)", version="1.1.0")

@app.get("/health")
async def health():
    return {"status": "ok", "use_ai": settings.use_ai and bool(settings.gemini_api_key)}

# Webhook verification (GET)
@app.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.whatsapp_verify_token and challenge:
        return challenge
    raise HTTPException(status_code=403, detail="Verification failed")

# Receive webhook (POST)
@app.post("/webhook")
async def receive_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None, alias="X-Hub-Signature-256"),
):
    body_bytes = await request.body()

    # Optional signature verification
    if not verify_x_hub_signature_256(settings.app_secret, body_bytes, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = await request.json()

    # WhatsApp wraps messages in entry->changes->value->messages
    try:
        changes = data.get("entry", [])[0].get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        contacts = value.get("contacts", [])
    except Exception:
        messages = []

    for msg in messages:
        from_number = msg.get("from")
        msg_type = msg.get("type")
        text_body = ""
        if msg_type == "text":
            text_body = msg.get("text", {}).get("body", "")

        # Use handler that may call AI
        if from_number and text_body:
            try:
                await handle_incoming_message(from_number, text_body)
            except Exception as e:
                print("Send error:", e)

    return {"status": "received"}

# Proactive outbound send
@app.post("/send/text")
async def send_text(req: SendTextRequest):
    try:
        res = await send_text_message(req.to, req.body)
        return {"success": True, "response": res}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
