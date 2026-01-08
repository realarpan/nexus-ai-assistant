"""Document schemas"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentResponse(BaseModel):
    id: int
    title: str
    file_type: Optional[str]
    file_size: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True