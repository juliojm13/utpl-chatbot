import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import patch
from app.interface.main import app

@pytest.mark.asyncio
@patch("app.infrastructure.llm.get_gemini_response", return_value="Hello from Gemini!")
@patch("httpx.AsyncClient.post", return_value=None)
async def test_telegram_webhook_start(mock_post, mock_gemini):
    payload = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "text": "/start",
            "date": 1710000000,
            "chat": {"id": 12345, "type": "private"},
            "from": {"id": 67890, "is_bot": False, "first_name": "Test"}
        }
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/webhook/telegram", json=payload)
    assert response.status_code == 200
    assert response.json() == {"ok": True}

@pytest.mark.asyncio
@patch("app.infrastructure.llm.get_gemini_response", return_value="Hello from Gemini!")
@patch("httpx.AsyncClient.post", return_value=None)
async def test_telegram_webhook_message(mock_post, mock_gemini):
    # First, start a conversation
    payload_start = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "text": "/start",
            "date": 1710000000,
            "chat": {"id": 12345, "type": "private"},
            "from": {"id": 67890, "is_bot": False, "first_name": "Test"}
        }
    }
    # Then, send a normal message
    payload_msg = {
        "update_id": 2,
        "message": {
            "message_id": 2,
            "text": "Hello, bot!",
            "date": 1710000001,
            "chat": {"id": 12345, "type": "private"},
            "from": {"id": 67890, "is_bot": False, "first_name": "Test"}
        }
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/webhook/telegram", json=payload_start)
        response = await ac.post("/webhook/telegram", json=payload_msg)
    assert response.status_code == 200
    assert response.json() == {"ok": True} 