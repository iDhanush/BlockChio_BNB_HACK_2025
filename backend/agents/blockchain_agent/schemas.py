from typing import TypedDict, Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    question: str
    response: Optional[str | dict]
    user_id: str

class TransferInput(BaseModel):
    to: str = Field(..., description="The address to transfer to")
    amount: float = Field(..., description="The amount to transfer in eth")

class NftInput(BaseModel):
    url: str = Field(..., description="The url of the nft")

class NoInput(BaseModel):
    pass
