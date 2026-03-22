import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.NOTION_TOKEN = os.getenv("NOTION_TOKEN")

        if not self.NOTION_TOKEN:
            raise ValueError("Missing NOTION_TOKEN")

        self.NOTION_HEADERS = {
            "Authorization": f"Bearer {self.NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

settings = Settings()