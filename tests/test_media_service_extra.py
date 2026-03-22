import os
import types


def make_sample_result(trakt_url=None):
    props = {
        "Metadata Filled": {"checkbox": False},
        "Name": {"title": [{"plain_text": "Sample"}]}
    }
    if trakt_url is not None:
        props["Trakt URL"] = {"url": trakt_url}
    return {"properties": props}


def test_enrich_handles_none_response(monkeypatch, caplog):
    import apis.notion_api as notion_api
    monkeypatch.setattr("services.media_service.read_database", lambda db, headers, payload: None)

    import services.media_service as media_service

    caplog.set_level("ERROR")
    media_service.enrich_notion_items()

    assert any("Failed to fetch data from Notion" in rec.message for rec in caplog.records)


def test_enrich_handles_empty_results(monkeypatch, caplog):
    import apis.notion_api as notion_api
    monkeypatch.setattr("services.media_service.read_database", lambda db, headers, payload: {"results": []})

    import services.media_service as media_service

    caplog.set_level("INFO")
    media_service.enrich_notion_items()

    assert any("No items found that need enrichment." in rec.message for rec in caplog.records)


def test_enrich_skips_items_without_trakt(monkeypatch, caplog):
    fake_results = [make_sample_result(None)]
    monkeypatch.setattr('services.media_service.read_database', lambda db, headers, payload: {"results": fake_results})

    import services.media_service as media_service

    caplog.set_level("DEBUG")
    media_service.enrich_notion_items()

    # Should process the item but not extract an ID
    assert any("Processing item" in rec.message or "processing" in rec.message.lower() for rec in caplog.records)
    assert not any("Extracted Trakt ID" in rec.message for rec in caplog.records)


def test_enrich_handles_trakt_with_trailing_slash(monkeypatch, caplog):
    fake_results = [make_sample_result("https://trakt.tv/movie/123/")]
    monkeypatch.setattr('apis.notion_api.read_database', lambda db, headers, payload: {"results": fake_results})

    import services.media_service as media_service

    caplog.set_level("DEBUG")
    media_service.enrich_notion_items()

    assert any("Extracted Trakt ID" in rec.message for rec in caplog.records)
