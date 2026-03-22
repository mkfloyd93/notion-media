from services.media_service import enrich_notion_items
from config.logging_config import setup_logging
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    setup_logging()
    enrich_notion_items()