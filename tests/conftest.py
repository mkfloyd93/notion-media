import pathlib
import os
from dotenv import load_dotenv

# Locate project root (one directory above tests/)
ROOT = pathlib.Path(__file__).resolve().parents[1]
DOTENV_PATH = ROOT / ".env"

# Load .env from project root if present so tests pick up env vars automatically
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=str(DOTENV_PATH))
else:
    # fallback to default load (in case .env is elsewhere)
    load_dotenv()

# Optionally ensure some defaults for tests (don't set real secrets)
os.environ.setdefault("NOTION_TOKEN", "test-token")
os.environ.setdefault("NOTION_MEDIA_DB_ID", "test-db")
