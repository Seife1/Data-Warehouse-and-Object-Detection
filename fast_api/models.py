from sqlalchemy import Column, BigInteger, String, DateTime
from fast_api.database import Base

class CleanedScrapedData(Base):
    __tablename__ = "cleaned_scraped_data"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    channel_title = Column(String)
    channel_username = Column(String)
    message = Column(String)
    date = Column(DateTime)
    media_path = Column(String)