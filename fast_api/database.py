from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get credentials from the environment
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Define a function that create the database engine
def create_db_engine(db_url):
    """
    Creates an SQLAlchemy engine for PostgreSQL using environment variables.

    :return: SQLAlchemy engine instance.
    """
    try:
        engine = create_engine(db_url)
        print("Database engine created successfully!")
        return engine
    except Exception as e:
        print(f"An error occurred while creating the database engine: {e}")
        return None

# Create an SQLAlchemy engine for PostgreSQL
db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_db_engine(db_url)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
