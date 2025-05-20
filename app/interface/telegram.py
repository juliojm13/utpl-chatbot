from fastapi import APIRouter, Depends, status, Request
from app.interface.schemas import TelegramUpdate
from app.application.use_cases import ChatService
from app.interface.dependencies import get_chat_service
from app.infrastructure.llm import get_gemini_response
import httpx
import os
import logging

router = APIRouter()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

logger = logging.getLogger("telegram_webhook")
logging.basicConfig(level=logging.INFO)

@router.post("/webhook/telegram", status_code=status.HTTP_200_OK)
async def telegram_webhook(request: Request, chat_service: ChatService = Depends(get_chat_service)):
    try:
        body = await request.body()
        logger.info(f"Incoming webhook body: {body}")
        update = TelegramUpdate.parse_raw(body)
    except Exception as e:
        logger.error(f"Failed to parse TelegramUpdate: {e}")
        return {"ok": False, "error": str(e)}

    if not update.message or not update.message.text:
        return {"ok": True}

    message = update.message
    telegram_id = str(message.from_["id"])
    text = message.text.strip()
    chat_id = message.chat["id"]

    user = chat_service.get_or_create_user(telegram_id)

    if text == "/start":
        # End any active conversation
        active_conv = chat_service.get_active_conversation(user.id)
        if active_conv:
            chat_service.end_conversation(active_conv.id)
        conversation = chat_service.start_conversation(user.id)
        reply = "Hola! ¿Cómo te puedo ayudar?"
        chat_service.add_message(conversation.id, "bot", reply)
    else:
        conversation = chat_service.get_active_conversation(user.id)
        if not conversation:
            conversation = chat_service.start_conversation(user.id)
        chat_service.add_message(conversation.id, "user", text)
        # Get conversation history for context
        history = chat_service.get_conversation_history(conversation.id)
        history_for_llm = [
            {"role": m.sender, "content": m.text} for m in history if m.sender in ("user", "bot")
        ]
        reply = get_gemini_response(text, history_for_llm)
        chat_service.add_message(conversation.id, "bot", reply)

    # Send reply to Telegram
    async with httpx.AsyncClient() as client:
        await client.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": reply
        })
    return {"ok": True} 