from sqlalchemy.orm import Session
from typing import Optional, List
from app.domain.entities import User, Conversation, Message
from app.domain.repositories import UserRepository, ConversationRepository, MessageRepository
from .models import UserDB, ConversationDB, MessageDB
from datetime import datetime

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_telegram_id(self, telegram_id: str) -> Optional[User]:
        user = self.db.query(UserDB).filter_by(telegram_id=telegram_id).first()
        if user:
            return User(id=user.id, telegram_id=user.telegram_id)
        return None

    def create(self, telegram_id: str) -> User:
        user_db = UserDB(telegram_id=telegram_id)
        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)
        return User(id=user_db.id, telegram_id=user_db.telegram_id)

class SQLAlchemyConversationRepository(ConversationRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_active_by_user(self, user_id: int) -> Optional[Conversation]:
        conv = self.db.query(ConversationDB).filter_by(user_id=user_id, ended_at=None).first()
        if conv:
            return Conversation(id=conv.id, user_id=conv.user_id, started_at=conv.started_at, ended_at=conv.ended_at)
        return None

    def create(self, user_id: int) -> Conversation:
        conv_db = ConversationDB(user_id=user_id)
        self.db.add(conv_db)
        self.db.commit()
        self.db.refresh(conv_db)
        return Conversation(id=conv_db.id, user_id=conv_db.user_id, started_at=conv_db.started_at, ended_at=conv_db.ended_at)

    def end_conversation(self, conversation_id: int) -> None:
        conv = self.db.query(ConversationDB).filter_by(id=conversation_id).first()
        if conv:
            conv.ended_at = datetime.utcnow()
            self.db.commit()

    def get_by_id(self, conversation_id: int) -> Optional[Conversation]:
        conv = self.db.query(ConversationDB).filter_by(id=conversation_id).first()
        if conv:
            return Conversation(id=conv.id, user_id=conv.user_id, started_at=conv.started_at, ended_at=conv.ended_at)
        return None

class SQLAlchemyMessageRepository(MessageRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_message(self, conversation_id: int, sender: str, text: str) -> Message:
        msg_db = MessageDB(conversation_id=conversation_id, sender=sender, text=text)
        self.db.add(msg_db)
        self.db.commit()
        self.db.refresh(msg_db)
        return Message(id=msg_db.id, conversation_id=msg_db.conversation_id, sender=msg_db.sender, text=msg_db.text, timestamp=msg_db.timestamp)

    def get_by_conversation(self, conversation_id: int) -> List[Message]:
        msgs = self.db.query(MessageDB).filter_by(conversation_id=conversation_id).order_by(MessageDB.timestamp).all()
        return [Message(id=m.id, conversation_id=m.conversation_id, sender=m.sender, text=m.text, timestamp=m.timestamp) for m in msgs] 