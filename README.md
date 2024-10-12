# Data Warehouse and Object Detection

## 1. Overview
This project builds a data warehouse for Ethiopian medical business data scraped from Telegram channels and applies object detection using YOLO on collected images.

## 2. Prerequisites
- Python 3.x
- PostgreSQL
- Telegram API key
- Clone the repository
```bash
git clone https://github.com/Seife1/Data-Warehouse-and-Object-Detection.git
```
- Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 3. Project Structure
```bash
root/
├── data/
│   ├── raw/           # Raw scraped data
│   ├── cleaned/       # Cleaned and transformed data
├── dbt/               # DBT models for data transformation
├── models/            # YOLO and database models
├── notebooks/         # Jupyter notebooks for analysis
├── scripts/           # Python scripts for scraping and ETL
├── fastapi/           # FastAPI application
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
├── logs/              # Log files
├── README.md
└── requirements.txt   # List of dependencies
```

## 4. Usage
**Data Scraping**

1. Set up Telegram API.
2. Run the scraping script:
```bash
python3 scripts/scrape_telegram.py
```




