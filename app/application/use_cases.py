from app.domain.repositories import UserRepository, ConversationRepository, MessageRepository
from app.domain.entities import User, Conversation, Message
from typing import List, Optional

class ChatService:
    def __init__(self, user_repo: UserRepository, conv_repo: ConversationRepository, msg_repo: MessageRepository):
        self.user_repo = user_repo
        self.conv_repo = conv_repo
        self.msg_repo = msg_repo

    def get_or_create_user(self, telegram_id: str) -> User:
        user = self.user_repo.get_by_telegram_id(telegram_id)
        if user:
            return user
        return self.user_repo.create(telegram_id)

    def start_conversation(self, user_id: int) -> Conversation:
        return self.conv_repo.create(user_id)

    def end_conversation(self, conversation_id: int) -> None:
        self.conv_repo.end_conversation(conversation_id)

    def get_active_conversation(self, user_id: int) -> Optional[Conversation]:
        return self.conv_repo.get_active_by_user(user_id)

    def add_message(self, conversation_id: int, sender: str, text: str) -> Message:
        return self.msg_repo.add_message(conversation_id, sender, text)

    def get_conversation_history(self, conversation_id: int) -> List[Message]:
        return self.msg_repo.get_by_conversation(conversation_id) 