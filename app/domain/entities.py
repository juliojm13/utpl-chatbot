from datetime import datetime
from typing import List, Optional

class User:
    def __init__(self, id: int, telegram_id: str):
        self.id = id
        self.telegram_id = telegram_id

class Conversation:
    def __init__(self, id: int, user_id: int, started_at: datetime, ended_at: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.started_at = started_at
        self.ended_at = ended_at
        self.messages: List[Message] = []  # type: ignore

class Message:
    def __init__(self, id: int, conversation_id: int, sender: str, text: str, timestamp: datetime):
        self.id = id
        self.conversation_id = conversation_id
        self.sender = sender  # 'user' or 'bot'
        self.text = text
        self.timestamp = timestamp 