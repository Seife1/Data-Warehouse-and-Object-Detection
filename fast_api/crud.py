import os
import csv
import glob
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from fast_api import models, schemas

# Set up logging
from scripts.logger_config import setup_logging
logger = setup_logging(log_file='./logs/crud.log')

# ==========================================
# CRUD operations on cleaned_scraped_data
# ==========================================
def create_item(db: Session, item: schemas.ItemCreate):
    logger.info(f"Creating new item with channel_title: {item.channel_title}")
    db_item = models.CleanedScrapedData(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Item created with ID: {db_item.id}")
    return db_item

def get_item(db: Session, item_id: int):
    logger.info(f"Fetching item with ID: {item_id}")
    item = db.query(models.CleanedScrapedData).filter(models.CleanedScrapedData.id == item_id).first()
    if item:
        logger.info(f"Item found: {item}")
    else:
        logger.warning(f"Item with ID: {item_id} not found")
    return item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching items with skip={skip}, limit={limit}")
    items = db.query(models.CleanedScrapedData).offset(skip).limit(limit).all()
    logger.info(f"Fetched {len(items)} items")
    return items

# ==========================================
# Warehouse Analytics & Metrics
# ==========================================
def get_channels(db: Session) -> List[schemas.ChannelSummary]:
    logger.info("Fetching distinct channels and message totals")
    results = (
        db.query(
            models.CleanedScrapedData.channel_title,
            models.CleanedScrapedData.channel_username,
            func.count(models.CleanedScrapedData.id).label("total_messages")
        )
        .group_by(models.CleanedScrapedData.channel_title, models.CleanedScrapedData.channel_username)
        .all()
    )
    return [
        schemas.ChannelSummary(
            channel_title=r.channel_title or "Unknown",
            channel_username=r.channel_username,
            total_messages=r.total_messages
        )
        for r in results
    ]

def get_analytics_summary(db: Session) -> List[schemas.AnalyticsSummary]:
    logger.info("Fetching analytics summary aggregated by channel")
    results = (
        db.query(
            models.CleanedScrapedData.channel_title,
            func.count(models.CleanedScrapedData.id).label("message_count"),
            func.min(models.CleanedScrapedData.date).label("first_message_date"),
            func.max(models.CleanedScrapedData.date).label("last_message_date")
        )
        .group_by(models.CleanedScrapedData.channel_title)
        .all()
    )
    return [
        schemas.AnalyticsSummary(
            channel_title=r.channel_title or "Unknown",
            message_count=r.message_count,
            first_message_date=r.first_message_date,
            last_message_date=r.last_message_date
        )
        for r in results
    ]

# ==========================================
# YOLO Object Detection Results
# ==========================================
def get_detections(label: Optional[str] = None, min_confidence: float = 0.0) -> List[schemas.DetectionResult]:
    logger.info(f"Querying YOLO detections (label={label}, min_confidence={min_confidence})")
    detections: List[schemas.DetectionResult] = []
    yolo_dir = os.path.join(os.path.dirname(__file__), "..", "YOLO")
    csv_files = glob.glob(os.path.join(yolo_dir, "*detections*.csv"))

    for filepath in csv_files:
        try:
            with open(filepath, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    conf = float(row.get("confidence", 0.0))
                    name = row.get("name", "").strip()
                    if conf < min_confidence:
                        continue
                    if label and label.lower() not in name.lower():
                        continue
                    detections.append(
                        schemas.DetectionResult(
                            name=name,
                            confidence=round(conf, 4),
                            xmin=float(row.get("xmin", 0.0)),
                            ymin=float(row.get("ymin", 0.0)),
                            xmax=float(row.get("xmax", 0.0)),
                            ymax=float(row.get("ymax", 0.0)),
                        )
                    )
        except Exception as e:
            logger.error(f"Error parsing detection file {filepath}: {e}")

    return detections
