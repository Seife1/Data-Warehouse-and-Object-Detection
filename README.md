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
### **Data Scraping**

1. Set up Telegram API.
    - Ensure you have your Telegram API credentials set up.
2. Run the scraping script:
```bash
python3 scripts/scrape_telegram.py
```
- This script will scrape data from the specified Telegram channels and store the raw data in the data/raw/ directory.

### **Data Cleaning**

After scraping the data, you'll need to clean it to ensure consistency and prepare it for transformation and analysis.

Run the Jupyter `notebook/1_Data_Cleaning.ipynb` to ensure your data is consistent and free of errors:

Steps:
- Ensures all data follows a consistent format for easier analysis.
- Removes duplicate rows.
- Drops rows where both Message and Media Path are NaN.
- Fills missing messages and media paths.

After cleaning, data will be exported to a table called cleaned_scraped_data in your **POSTGRESQL** database.

    Note: You can check the detailed logs in logs/data_preparation.log for the cleaning process.

### **Data Transformation**

The data transformation process leverages DBT (Data Build Tool) to perform complex transformations and modeling on the cleaned data stored in the PostgreSQL database.

The DBT project for this pipeline is located in the `./dbt/Ethio_Medical_Business/` directory. This project uses DBT to define and run transformations, ensuring the data is structured for efficient analysis.

For more detailed instructions on how to set up and use DBT for this project, refer to the [Ethio Medical Business DBT Project README](./dbt/Ethio_Medical_Business/README.md).

**Overview of DBT Workflow:**
1. Install and configure DBT.
2. Define transformations using DBT models.
3. Run DBT commands to transform the data.
4. Test and document the transformations for accuracy and transparency.

For an in-depth guide, check the linked [README](./dbt/Ethio_Medical_Business/README.md).


