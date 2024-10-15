import sys
import os

# Set up logging
from scripts.logger_config import setup_logging

# Set up logging
logger = setup_logging(log_file='./logs/crud.log',)

sys.path.append("fastapi")

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fast_api.database import engine, get_db
from fast_api import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    new_item = crud.create_item(db=db, item=item)
    print(new_item)
    return new_item

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    logger.info(f"Items: {items}")
    if not items:  # If no valid_items found
        raise HTTPException(status_code=404, detail="No items found")
    return items
