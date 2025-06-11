from pydantic import BaseModel, Field
from typing import List, Optional

class Link(BaseModel):
    url: str
    text: str

class AskRequest(BaseModel):
    question: str = Field(..., description="The student's question.")
    image: Optional[str] = Field(None, description="Base64-encoded image attachment.")

class AskResponse(BaseModel):
    answer: str
    links: List[Link]