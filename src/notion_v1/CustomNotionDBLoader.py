from langchain.document_loaders.notiondb import (
    NotionDBLoader, PAGE_URL
)
from langchain.docstore.document import Document
from typing import Dict, Any


class CustomNotionDBLoader(NotionDBLoader):
    def load_page(self, page_id: str) -> Document:
        """Read a page."""
        data = self._request(PAGE_URL.format(page_id=page_id))

        # load properties as metadata
        metadata: Dict[str, Any] = {}

        for prop_name, prop_data in data["properties"].items():
            prop_type = prop_data["type"]

            if prop_type == "rich_text":
                value = (
                    prop_data["rich_text"][0]["plain_text"]
                    if prop_data["rich_text"]
                    else None
                )
            elif prop_type == "title":
                value = (
                    prop_data["title"][0]["plain_text"] if prop_data["title"] else None
                )
            elif prop_type == "multi_select":
                value = (
                    [item["name"] for item in prop_data["multi_select"]]
                    if prop_data["multi_select"]
                    else []
                )
            elif prop_type == "url":
                value = prop_data["url"]
            elif prop_type == "relation":
                value = prop_data['relation']
            elif prop_type == 'checkbox':
                value = prop_data['checkbox']
            else:
                value = None

            if value is not None:
                metadata[prop_name.lower()] = value

        metadata["id"] = page_id

        page_content = self._load_blocks(page_id)
        if page_content == '':
            page_content = metadata['name']
        return Document(page_content=page_content, metadata=metadata)
