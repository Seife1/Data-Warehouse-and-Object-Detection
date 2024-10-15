from sqlalchemy.orm import Session
from fast_api import models, schemas


# Set up logging
from scripts.logger_config import setup_logging

# Set up logging
logger = setup_logging(log_file='./logs/crud.log',)

# Create a new item (record) in the cleaned_scraped_data table
def create_item(db: Session, item: schemas.ItemCreate):
    logger.info(f"Creating new item with channel_title: {item.channel_title}")
    db_item = models.CleanedScrapedData(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Item created with ID: {db_item.id}")
    return db_item

# Get an item by ID
def get_item(db: Session, item_id: int):
    logger.info(f"Fetching item with ID: {item_id}")
    item = db.query(models.CleanedScrapedData).filter(models.CleanedScrapedData.id == item_id).first()
    if item:
        logger.info(f"Item found: {item}")
    else:
        logger.warning(f"Item with ID: {item_id} not found")
    return item

# Get multiple items (records) with optional pagination (skip and limit)
def get_items(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching items with skip={skip}, limit={limit}")
    items = db.query(models.CleanedScrapedData).offset(skip).limit(limit).all()
    logger.info(f"Fetched {len(items)} items")
    return items
