from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    query: str
    assistant_id: Optional[str] = None
    thread_id: Optional[str] = None
