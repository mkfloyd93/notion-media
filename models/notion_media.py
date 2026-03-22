class NotionMediaItem:
    def __init__(self, raw: dict):
        self.raw = raw
        self.properties = raw.get("properties", {})

    def _get(self, prop_name, field="rich_text"):
        """Generic property getter based on Notion structure.

        Returns the requested field value when the property is a dict and the
        field is present. Otherwise returns None.
        """
        prop = self.properties.get(prop_name)
        if not isinstance(prop, dict):
            return None
        return prop.get(field)

    @property
    def trakt_url(self):
        return self._get("Trakt URL", "url")

    @property
    def metadata_filled(self):
        return self._get("Metadata Filled", "checkbox")

    @property
    def title(self):
        title_data = self._get("Name", "title") or []
        if isinstance(title_data, list) and title_data:
            return title_data[0].get("plain_text")
        return None