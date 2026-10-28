import os
import sys
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Ensure root workspace directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "medical_warehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

if DB_PASSWORD:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

class CleanedScrapedData(Base):
    __tablename__ = "cleaned_scraped_data"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    channel_title = Column(String)
    channel_username = Column(String)
    message = Column(String)
    date = Column(DateTime)
    media_path = Column(String)


SAMPLE_RECORDS = [
    {
        "channel_title": "CheMed Medical Supplies",
        "channel_username": "@CheMed123",
        "message": "Paracetamol 500mg syrup and tablets restocked. Bulk wholesale available. Price: 450 ETB per pack. Contact +251911000000.",
        "date": datetime(2024, 7, 10, 8, 30, tzinfo=timezone.utc),
        "media_path": "media/@CheMed123_76.jpg"
    },
    {
        "channel_title": "Doctors Ethiopia Medical Network",
        "channel_username": "@DoctorsET",
        "message": "Clinical Advisory: Managing pediatric hydration during dry season. Early identification of dehydration signs saves lives.",
        "date": datetime(2024, 7, 11, 14, 15, tzinfo=timezone.utc),
        "media_path": None
    },
    {
        "channel_title": "East Africa Health Care Initiative",
        "channel_username": "@EAHCI",
        "message": "Digital ultrasound scanners and medical diagnostic equipment arriving at Addis Ababa customs. Inquiries open for private clinics.",
        "date": datetime(2024, 7, 12, 11, 0, tzinfo=timezone.utc),
        "media_path": "media/@EAHCI_2377.jpg"
    },
    {
        "channel_title": "Lobelia Dermo Cosmetics",
        "channel_username": "@lobelia4cosmetics",
        "message": "Dermatologist recommended CeraVe moisturizing cream 453g. Original from France. Special promo 1,850 Birr with free delivery.",
        "date": datetime(2024, 7, 13, 16, 45, tzinfo=timezone.utc),
        "media_path": "media/@lobelia4cosmetics_12432.jpg"
    },
    {
        "channel_title": "Yetenaweg Medical Hub",
        "channel_username": "@yetenaweg",
        "message": "Preventive Cardiology: 5 lifestyle changes to control hypertension without increasing medication dosages. Read the full summary.",
        "date": datetime(2024, 7, 14, 9, 20, tzinfo=timezone.utc),
        "media_path": "media/@yetenaweg_1160.jpg"
    },
    {
        "channel_title": "CheMed Medical Supplies",
        "channel_username": "@CheMed123",
        "message": "Surgical latex gloves (Sizes S, M, L) and N95 masks now in stock. Wholesale order hotline active.",
        "date": datetime(2024, 7, 15, 10, 10, tzinfo=timezone.utc),
        "media_path": "media/@CheMed123_80.jpg"
    },
    {
        "channel_title": "Lobelia Dermo Cosmetics",
        "channel_username": "@lobelia4cosmetics",
        "message": "La Roche-Posay Anthelios SPF 50+ Sunscreen milk. Certified hypoallergenic. Price: 2,400 ETB. Limited quantity.",
        "date": datetime(2024, 7, 16, 12, 0, tzinfo=timezone.utc),
        "media_path": "media/@lobelia4cosmetics_12435.jpg"
    }
]


def init_database():
    print(f"Connecting to PostgreSQL warehouse at {DB_HOST}:{DB_PORT}/{DB_NAME}...")
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        count = session.query(CleanedScrapedData).count()
        print(f"Current record count in 'cleaned_scraped_data': {count}")

        if count == 0:
            print("Populating initial Ethiopian medical Telegram messages...")
            for rec in SAMPLE_RECORDS:
                item = CleanedScrapedData(**rec)
                session.add(item)
            session.commit()
            print(f"Successfully seeded {len(SAMPLE_RECORDS)} baseline records!")
        else:
            print("Database already contains data. Skipping initial seed.")

        session.close()
        print("Database initialization complete.")
    except Exception as e:
        print(f"Warning: Could not connect or seed database: {e}")
        print("Note: If running outside Docker without local PostgreSQL, start the container via 'docker compose up'.")


if __name__ == "__main__":
    init_database()
