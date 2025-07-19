from pydantic import BaseModel
from typing import Optional, Any, Union


class StandardResponse(BaseModel):
    status: str = 'success'
    code: int = 200
    message: Optional[str] = None
    data: Optional[Any] = None


class StandardException(Exception):
    def __init__(self, status_code: int, details: Union[str, list], message: str = ""):
        if not isinstance(details, list):
            details = [details]
        self.details = details
        self.message = message
        self.status_code = status_code
