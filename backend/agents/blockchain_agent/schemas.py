from typing import TypedDict, Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    question: str
    response: Optional[str | dict]
    user_id: str


class TransferInput(BaseModel):
    to: str = Field(..., description="The address to transfer to")
    amount: int = Field(..., description="The amount to transfer")


class NoInput(BaseModel):
    pass
