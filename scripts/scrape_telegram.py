from dotenv import load_dotenv
import os
import csv
import json
from telethon import TelegramClient

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')

# Set up logging
from logger_config import setup_logging

# Set up logging
logger = setup_logging(log_file='./logs/scrape_telegram.log',)

# Set up Telegram client with scrapping session file
client = TelegramClient('scrapping_session', api_id, api_hash)

# Function to get the last message ID
def get_last_id(channel_username):
    """
    Retrieve the last message ID for a given Telegram channel.

    This function reads a JSON file named '{channel_username}_last_id.json' located in the './data/raw/' directory.
    The JSON file is expected to contain a key 'last_id' which holds the last message ID. If the file or the key
    does not exist, the function returns 0.

    Args:
        channel_username (str): The username of the Telegram channel.

    Returns:
        int: The last message ID if found, otherwise 0.
    """
    try:
        with open('./data/raw/{channel_username}_last_id.json', 'r') as f:
            last_id = json.load(f).get('last_id', 0)
            return last_id
    except FileNotFoundError:
        logger.warning(f"File {channel_username}_last_id.json not found")   
        return 0
    
# Function to save the last message ID
def save_last_id(channel_username, last_id):
    """
    Save the last message ID for a given Telegram channel to a JSON file.

    Args:
        channel_username (str): The username of the Telegram channel.
        last_id (int): The last message ID to be saved.

    Writes:
        A JSON file named '{channel_username}_last_id.json' in the './data/raw/' directory
        containing the last message ID.
    """
    with open(f'./data/raw/{channel_username}_last_id.json', 'w') as f:
        json.dump({'last_id': last_id}, f)
        logger.info(f"Saved last_id {last_id} for {channel_username}")  

# Function to scrape a channel
async def scrape_channel(client, channel_username, writer, media_dir):
    """
    Scrapes messages from a specified Telegram channel and writes the data to a CSV file.

    Args:
        client (TelegramClient): The Telegram client instance.
        channel_username (str): The username of the Telegram channel to scrape.
        writer (csv.writer): The CSV writer object to write the scraped data.
        media_dir (str): The directory where media files will be saved.

    Writes:
        CSV file with the following columns:
            - Channel Title
            - Channel Username
            - Message ID
            - Message Text
            - Message Date
            - Media Path (if any)

    Logs:
        - Information about downloaded media files.
        - Errors encountered during the scraping process.
    """
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title

        last_id = get_last_id(channel_username)

        # Get the messages from the channel
        # We will get the last 10 messages

        async for message in client.iter_messages(entity, limit=20, offset_id=last_id):
            if message.media:
                filename = f"{channel_username}_{message.id}.{message.media.document.mime_type.split('/')[-1]}" if hasattr(message.media, 'document') else f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await message.download_media(media_path)
                logger.info(f"Downloaded media for message {message.id}")
            else:
                media_path = None

            writer.writerow([channel_title, channel_username, message.id, message.text, message.date, media_path])
            save_last_id(channel_username, message.id)
    except Exception as e:
        logger.error(f"Error in scrape_channel function: {e}")

async def main():
    try:
        await client.start(phone)
        logger.info("Client started")

        media_dir = 'media'
        os.makedirs(media_dir, exist_ok=True)

        with open('./data/raw/scraped_data.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['channel_title', 'channel_username', 'id', 'message', 'date', 'media_path'])

            channels = [
                '@yetenaweg',
                '@CheMed123',
                '@lobelia4cosmetics',
                '@DoctorsET',
                '@EAHCI'
            ]

            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir)
                logger.info(f"Scraped {channel}")

    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())