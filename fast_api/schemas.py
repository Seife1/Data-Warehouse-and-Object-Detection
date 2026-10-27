from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ==========================================
# Scraped Message Schemas (CRUD)
# ==========================================
class ItemBase(BaseModel):
    channel_title: str
    channel_username: str
    message: str
    date: datetime
    media_path: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# ==========================================
# Warehouse Analytics & Channel Schemas
# ==========================================
class ChannelSummary(BaseModel):
    channel_title: str
    channel_username: Optional[str] = None
    total_messages: int

class AnalyticsSummary(BaseModel):
    channel_title: str
    message_count: int
    first_message_date: Optional[datetime] = None
    last_message_date: Optional[datetime] = None

# ==========================================
# YOLO Object Detection Schemas
# ==========================================
class DetectionResult(BaseModel):
    name: str
    confidence: float
    xmin: float
    ymin: float
    xmax: float
    ymax: float

# ==========================================
# Service Health Schema
# ==========================================
class HealthResponse(BaseModel):
    status: str
    database: str
    version: str
