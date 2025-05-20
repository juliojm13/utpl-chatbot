from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db import SessionLocal
from app.infrastructure.repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyConversationRepository,
    SQLAlchemyMessageRepository,
)
from app.application.use_cases import ChatService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    user_repo = SQLAlchemyUserRepository(db)
    conv_repo = SQLAlchemyConversationRepository(db)
    msg_repo = SQLAlchemyMessageRepository(db)
    return ChatService(user_repo, conv_repo, msg_repo) 