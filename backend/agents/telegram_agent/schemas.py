from typing import TypedDict, Any, Optional, List

from pydantic import BaseModel, Field


class AgentState(TypedDict):
    messages: list[dict[str, Any]]
    question: str
    response: Optional[str | dict]
    user_id: str


class TelegramTextInput(BaseModel):
    user_id: int = Field(..., description="The Telegram userid of recipient")
    text: str = Field(..., description="The text for sending message in Telegram")


class TelegramImageInput(BaseModel):
    user_id: int = Field(..., description="The Telegram user_id of recipient")
    image_url: str = Field(..., description="The URL for sending image in Telegram")
