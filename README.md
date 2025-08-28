<<<<<<< HEAD
# whatsapp-AI-Bot
for business
=======
# WhatsApp Business Cloud API Bot (FastAPI, Python) — Gemini-enabled

This project is the WhatsApp Business Cloud API bot with optional **Gemini (Google GenAI)** integration for intelligent replies.

## Highlights
- FastAPI webhook for WhatsApp Cloud API
- Optional Gemini integration (Google GenAI SDK)
- System prompt file under `prompts/assistant.txt`
- Toggle AI with `USE_AI` env var
- Dockerfile, .env.example, and sample endpoints

## How AI integration works
- Incoming messages are passed through a system prompt + user message to Gemini.
- Gemini's reply is sent back to the user via WhatsApp Cloud API.
- If `USE_AI=false` the bot falls back to echo behavior.

See `.env.example` for required environment variables.

>>>>>>> fc7582e (Initial commit for WhatsApp AI Bot project)
