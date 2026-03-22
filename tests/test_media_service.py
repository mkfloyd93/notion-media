import os
import types

import pytest


# Ensure the NOTION_TOKEN is present before importing settings-backed modules
os.environ.setdefault("NOTION_TOKEN", "fake-token")
os.environ.setdefault("NOTION_MEDIA_DB_ID", "fake-db")


def make_sample_result(trakt_url):
    return {
        "properties": {
            "Trakt URL": {"url": trakt_url},
            "Metadata Filled": {"checkbox": False},
            "Name": {"title": [{"plain_text": "Sample"}]}
        }
    }


def test_enrich_notion_items_calls_read_database(monkeypatch, caplog):
    # Prepare a fake response from read_database
    fake_results = [make_sample_result("https://trakt.tv/movie/123")]
    fake_response = {"results": fake_results}

    fake_module = types.SimpleNamespace()

    def fake_read_database(database_id, headers, payload):
        assert database_id == os.environ["NOTION_MEDIA_DB_ID"]
        assert isinstance(payload, dict)
        return fake_response

    # Monkeypatch the read_database function in the apis.notion_api module
    import apis.notion_api as notion_api

    monkeypatch.setattr(notion_api, "read_database", fake_read_database)

    # Import the service and run the function
    import services.media_service as media_service

    caplog.set_level("INFO")
    media_service.enrich_notion_items()

    # Verify logs show processing finished
    assert any("Finished processing Notion items." in rec.message or "processing" in rec.message.lower() for rec in caplog.records)
