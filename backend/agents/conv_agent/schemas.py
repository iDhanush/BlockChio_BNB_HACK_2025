from typing import TypedDict, List, Optional, Dict, Any
from pydantic import BaseModel


class RagInput(BaseModel):
    query: str

class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    question: str
    response: Optional[str | dict]
    user_id: str