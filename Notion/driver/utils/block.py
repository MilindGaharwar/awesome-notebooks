from abc import ABC, abstractmethod
from typing import Dict
from .request import RequestBlock
from .connect import Notion


class Block(ABC):
    type = None

    def __init__(self, dictionary: Dict) -> None:
        self.object = dictionary.get("object")
        self.id = dictionary.get("id")
        self.type = dictionary.get("type")
        self.created_time = dictionary.get("created_time")
        self.last_edited_time = dictionary.get("last_edited_time")
        self.has_children = dictionary.get("has_children")
        self.value = dictionary.get(self.type)

    def __repr__(self) -> str:
        return self.get()

    @abstractmethod
    def get(self):
        "Implemented in the subclass"

    @abstractmethod
    def set(self, value):
        "Implemented in the subclass"

    @abstractmethod
    def create(self, value):
        "Implemented in the subclass"

    def update(self):
        data = {self.type: self.value}
        RequestBlock(self.id, Notion.headers).update(data)

    def delete(self):
        RequestBlock(self.id, Notion.headers).delete()


# TODO: add a rich text object
class TextBLock(Block):
    type = None

    def get(self):
        content = [rich_text["plain_text"] for rich_text in self.value["text"]]
        return " ".join(content)

    def set(self, value: str):
        del self.value["text"][1:]
        self.value["text"][0]["text"]["content"] = value
        self.value["text"][0]["plain_text"] = value

    @classmethod
    def create(cls, text: str, link: str = None):
        return {
            "type": cls.type,
            cls.type: {
                "text": [{"type": "text", "text": {"content": text, "link": link}}]
            },
        }


class Paragraph(TextBLock):
    type = "paragraph"


class Heading1(TextBLock):
    type = "heading_1"


class Heading2(TextBLock):
    type = "heading_2"


class Heading3(TextBLock):
    type = "heading_3"


class BulletedList(TextBLock):
    type = "bulleted_list_item"


class NumberedList(TextBLock):
    type = "numbered_list_item"


class ToDo(TextBLock):
    type = "to_do"


class Toggle(TextBLock):
    type = "toggle"


class ChildPage:
    type = "child_page"


class Embed(Block):
    type = "embed"

    def get(self):
        return self.value["url"]

    def set(self, value):
        self.value["url"] = value

    @staticmethod
    def create(url: str):
        return {"type": "embed", "embed": {"url": url}}


mapping = {
    "paragraph": Paragraph,
    "heading_1": Heading1,
    "heading_2": Heading2,
    "heading_3": Heading3,
    "bulleted_list_item": BulletedList,
    "numbered_list_item": NumberedList,
    "to_do": ToDo,
    "toggle": Toggle,
    "child_page": ChildPage,
    "embed": Embed,
}


def extract_block(block_object):
    block_type = block_object.get("type")
    return mapping[block_type](block_object)  # .get()


def insert_block(block_object, value):
    block_type = block_object.get("type")
    return mapping[block_type](block_object).set(value)


if __name__ == "__main__":
    block_example = {
        "type": "heading_1",
        "heading_1": {
            "text": [
                {
                    "type": "text",
                    "text": {"content": "I am a Heading 1", "link": None},
                    "plain_text": "I am a Heading 1",
                    "href": None,
                }
            ]
        },
    }
