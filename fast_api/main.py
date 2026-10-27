import sys
import os
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

# Ensure root workspace directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.logger_config import setup_logging
logger = setup_logging(log_file='./logs/crud.log')

from fast_api.database import engine, get_db
from fast_api import crud, models, schemas

# Initialize database schema if database is available
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning(f"Database schema initialization skipped or failed: {e}")

app = FastAPI(
    title="Ethiopian Medical Data Warehouse & YOLO Object Detection API",
    description=(
        "Production-grade RESTful API serving scraped Telegram medical channels, "
        "dbt dimensional aggregations, and YOLOv5 computer vision detection results."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==========================================
# Root & Service Health
# ==========================================
@app.get("/", tags=["System"])
def read_root():
    return {
        "service": "Ethiopian Medical Data Warehouse & Detection API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "messages_crud": "/items/",
            "channels": "/api/v1/channels",
            "analytics_summary": "/api/v1/analytics/summary",
            "yolo_detections": "/api/v1/detections"
        }
    }

@app.get("/health", response_model=schemas.HealthResponse, tags=["System"])
def check_health(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Health check database ping failed: {e}")
        db_status = f"disconnected: {str(e)}"
    
    return schemas.HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        database=db_status,
        version="1.0.0"
    )

# ==========================================
# Scraped Messages (Backwards Compatible CRUD)
# ==========================================
@app.post("/items/", response_model=schemas.Item, status_code=201, tags=["Messages CRUD"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    new_item = crud.create_item(db=db, item=item)
    return new_item

@app.get("/items/{item_id}", response_model=schemas.Item, tags=["Messages CRUD"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=List[schemas.Item], tags=["Messages CRUD"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

# ==========================================
# Data Warehouse & DBT Analytics Endpoints
# ==========================================
@app.get("/api/v1/channels", response_model=List[schemas.ChannelSummary], tags=["Warehouse Analytics"])
def list_channels(db: Session = Depends(get_db)):
    """List all scraped medical channels and their total message volumes."""
    try:
        channels = crud.get_channels(db)
        return channels
    except Exception as e:
        logger.error(f"Error listing channels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/summary", response_model=List[schemas.AnalyticsSummary], tags=["Warehouse Analytics"])
def get_channel_summary(db: Session = Depends(get_db)):
    """Retrieve aggregate metrics (message count, earliest/latest date) per channel, mirroring DBT models."""
    try:
        summary = crud.get_analytics_summary(db)
        return summary
    except Exception as e:
        logger.error(f"Error fetching analytics summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# Multimodal Computer Vision (YOLO) Endpoints
# ==========================================
@app.get("/api/v1/detections", response_model=List[schemas.DetectionResult], tags=["YOLO Computer Vision"])
def list_detections(
    label: Optional[str] = Query(None, description="Filter detections by object class (e.g. 'person', 'bottle')"),
    min_confidence: float = Query(0.0, ge=0.0, le=1.0, description="Minimum confidence threshold (0.0 to 1.0)")
):
    """Query YOLOv5 detection outputs extracted from scraped medical images."""
    try:
        detections = crud.get_detections(label=label, min_confidence=min_confidence)
        return detections
    except Exception as e:
        logger.error(f"Error fetching YOLO detections: {e}")
        raise HTTPException(status_code=500, detail=str(e))
