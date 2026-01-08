"""User schemas"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    
    class Config:
        from_attributes = True