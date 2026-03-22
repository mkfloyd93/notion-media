import pytest
from models.notion_media import NotionMediaItem


def make_raw(trakt_url=None, metadata_filled=None, title=None):
    props = {}
    if trakt_url is not None:
        props["Trakt URL"] = {"url": trakt_url}
    if metadata_filled is not None:
        props["Metadata Filled"] = {"checkbox": metadata_filled}
    if title is not None:
        props["Name"] = {"title": [{"plain_text": title}]}
    return {"properties": props}


def test_trakt_url_present():
    raw = make_raw(trakt_url="https://trakt.tv/movie/123")
    item = NotionMediaItem(raw)
    assert item.trakt_url == "https://trakt.tv/movie/123"


def test_trakt_url_missing():
    raw = make_raw()
    item = NotionMediaItem(raw)
    assert item.trakt_url is None


def test_metadata_filled_true():
    raw = make_raw(metadata_filled=True)
    item = NotionMediaItem(raw)
    assert item.metadata_filled is True


def test_title_parsing():
    raw = make_raw(title="A Great Movie")
    item = NotionMediaItem(raw)
    assert item.title == "A Great Movie"


def test_malformed_properties_do_not_raise():
    raw = {"properties": {"Trakt URL": "not-a-dict"}}
    item = NotionMediaItem(raw)
    assert item.trakt_url is None
    assert item.title is None
    assert item.metadata_filled is None
