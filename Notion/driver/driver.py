from utils.request import RequestPage, RequestBlock
from utils.page import PageProperties, PageContent
from typing import Dict
from utils.connect import Notion


class Page:
    def __init__(self, page_url) -> None:
        self.url = page_url
        self.id = page_url.split("-")[-1]

        self._properties = RequestPage(Notion.headers, self.id).retreive()
        self.created_time = self._properties["created_time"]
        self.last_edited_time = self._properties["last_edited_time"]
        self.archived = self._properties["archived"]
        self.icon = self._properties["icon"]
        self.cover = self._properties["cover"]
        self.properties = PageProperties(self._properties, Notion.headers)
        self.parent = self._properties["parent"]

        self._content = RequestBlock(Notion.headers, self.id).retreive_children()
        self.content = PageContent(self._content, self.id, Notion.headers)

    def refresh(self):
        """Retreive Page properties & content."""
        return self.__init__(self.url)

    def delete(self):
        """Archiving workspace level pages via API not supported."""
        RequestBlock(Notion.headers, self.id).delete()

    # def duplicate(self):
    #     template = TemplateObject(self, self.content.raw, self.token_api).create()
    #     new_page = json.dumps(template)
    #     RequestPage(self.id, self.token_api).create(new_page)


if __name__ == "__main__":

    from utils.block import *

    TOKEN_API = "secret_R1CrUGn8bx9itbJW0Fc9Cc0R9Lmhbnz2ayqEe0GhRPq"
    PAGE_URL = "https://www.notion.so/Axel-2ccdafe28955478b8c9d70bda0044c86"

    Notion.connect(TOKEN_API)
    page = Page(PAGE_URL)
