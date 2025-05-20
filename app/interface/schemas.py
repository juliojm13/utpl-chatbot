from pydantic import BaseModel, Field
from typing import Optional

class TelegramMessage(BaseModel):
    message_id: int
    text: Optional[str]
    date: int
    chat: dict
    from_: dict = Field(alias="from")

    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }

class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] 