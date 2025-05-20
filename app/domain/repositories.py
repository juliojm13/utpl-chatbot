from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import User, Conversation, Message

class UserRepository(ABC):
    @abstractmethod
    def get_by_telegram_id(self, telegram_id: str) -> Optional[User]:
        pass
    @abstractmethod
    def create(self, telegram_id: str) -> User:
        pass

class ConversationRepository(ABC):
    @abstractmethod
    def get_active_by_user(self, user_id: int) -> Optional[Conversation]:
        pass
    @abstractmethod
    def create(self, user_id: int) -> Conversation:
        pass
    @abstractmethod
    def end_conversation(self, conversation_id: int) -> None:
        pass
    @abstractmethod
    def get_by_id(self, conversation_id: int) -> Optional[Conversation]:
        pass

class MessageRepository(ABC):
    @abstractmethod
    def add_message(self, conversation_id: int, sender: str, text: str) -> Message:
        pass
    @abstractmethod
    def get_by_conversation(self, conversation_id: int) -> List[Message]:
        pass 