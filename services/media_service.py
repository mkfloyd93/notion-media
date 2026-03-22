from apis.notion_api import read_database
from models.notion_media import NotionMediaItem
from config.settings import settings
from urllib.parse import urlparse
import os
import logging

logger = logging.getLogger(__name__)


def enrich_notion_items():
    logger.info("Enriching Notion items with media information...")
    
    payload = {
        "filter": {
            "property": "Metadata Filled",
            "checkbox": {
                "equals": False 
            }
        },
    }

    media_database_id = os.getenv("NOTION_MEDIA_DB_ID")
    return_data = read_database(media_database_id, settings.NOTION_HEADERS, payload)

    if not return_data:
        logger.error("Failed to fetch data from Notion")
        return

    results = return_data.get("results", [])

    if not results:
        logger.info("No items found that need enrichment.")
        return

    logger.info(f"Found {len(results)} items to enrich.")

    media_items = [NotionMediaItem(item) for item in results]

    for media_item in media_items:
        trakt_url = media_item.trakt_url
        logger.debug("Processing item", extra={"trakt_url": trakt_url})

        if trakt_url and trakt_url.startswith("https://trakt.tv/"):
            path = urlparse(trakt_url).path.strip("/")
            trakt_id = path.split("/")[-1]
            logger.debug(f"Extracted Trakt ID: {trakt_id}")
            # fetch media info here later

    logger.info("Finished processing Notion items.")