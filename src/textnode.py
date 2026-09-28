from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    LI = "li"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.PLAIN:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case TextType.LI:
                return LeafNode("li", self.text)

    def __eq__(self, other: TextNode) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        if self.url:
            return f'TextNode("{self.text}", {self.text_type}, "{self.url}")'
        else:
            return f'TextNode("{self.text}", {self.text_type}, {self.url})'
