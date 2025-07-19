from typing import TypedDict, Any, Optional

from pydantic import BaseModel, Field


class AgentState(TypedDict):
    messages: list[dict[str, Any]]
    question: str
    response: Optional[str | dict]
    user_id: str


class WhatsappTextInput(BaseModel):
    number: int = Field(..., description="The Whatsapp number of recipient")
    text: str = Field(..., description="The text for sending message in Whatsapp")


class WhatsappImageInput(BaseModel):
    number: int = Field(..., description="The Whatsapp number of recipient")
    image_url: str = Field(..., description="The URL for sending image in Whatsapp")
