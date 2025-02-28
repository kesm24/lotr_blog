import re
from enum import Enum

class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __eq__(self, other: object) -> bool:

        return (
            isinstance(other, TextNode) and
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

def extract_markdown_images(markdown: str) -> list[tuple[str, str]]:
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", markdown)

    return images

def extract_markdown_links(markdown: str) -> list[tuple[str, str]]:
    links = re.findall(r"\[(.*?)\]\((.*?)\)", markdown)

    return links

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for (text, url) in links:
            sections = remaining_text.split(f"[{text}]({url})", maxsplit=1)

            if len(sections) != 2:
                continue

            [before_text, after_text] = sections

            if before_text != "":
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(text, TextType.LINK, url))

            remaining_text = after_text

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)

        if len(sections) == 1:
            new_nodes.append(node)
            continue

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown syntax")

        for i, section in enumerate(sections):
            if section == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes