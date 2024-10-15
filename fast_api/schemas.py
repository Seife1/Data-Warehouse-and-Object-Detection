from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema shared between reading and creating
class ItemBase(BaseModel):
    channel_title: str  # Maps to "Channel Title"
    channel_username: str  # Maps to "Channel Username"
    message: str  # Maps to "Message"
    date: datetime  # Maps to "Date"
    media_path: Optional[str] = None  # Maps to "Media Path" (optional)

# Schema for creating a new item (does not require `id`)
class ItemCreate(ItemBase):
    pass

# Schema for reading data (includes `id`)
class Item(ItemBase):
    id: int  # The 'id' field is required for reading

    class Config:
        from_attributes = True  # Correctly allows Pydantic to work with SQLAlchemy models
