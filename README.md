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

### **Object Detection**

The object detection step is performed using a script in `notebooks/2_YOLO_ObjectDetection.ipynb`, utilizing the YOLOv5 algorithm implemented in `PyTorch`. YOLO (You Only Look Once) is an open-source software tool known for its efficiency in real-time object detection from images. The images for this project are collected from various Telegram channels through scraping.

#### Model Setup:
To set up the YOLOv5 model, follow these steps:
```bash
# Clone the YOLOv5 repository
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
# Install the necessary dependencies
pip install -r requirements.txt
```

The detection results are stored in the `YOLO` folder for integration and enrichment into the larger data pipeline.

For each series of images:
- Multiple objects are detected in each image, with labels such as `people`, `bottles`, and other items being identified.
- Confidence levels for the detected objects vary, meaning the model is more certain about some objects than others.
- In some cases, no objects were detected, resulting in empty detection outputs for those images.

The results, including labels, confidence scores, and bounding box coordinates, are saved as CSV files in the specified `YOLO` directory. These CSV files are used for further analysis and can be integrated into the data enrichment pipeline.

### **FastAPI Application**

The FastAPI application is responsible for managing the scraped data from Telegram channels. It provides full CRUD (Create, Read, Update, Delete) functionality, enabling users to interact with the PostgreSQL database through various API endpoints. The application handles data validation using Pydantic and ensures smooth database interactions with SQLAlchemy.

For more details on setting up and using the FastAPI application, please refer to the [FastAPI README](./fast_api/README.md).

## 5. Logging
Check logs in the logs/ folder.

## 6. License
MIT [License](LICENCE).
