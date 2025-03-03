# def main(hello: str) -> str:
#     print(hello)
#     return hello

# main("Hello World")

from blocks import block_to_block_type, markdown_to_blocks
from htmlnode import block_to_html_node


def extract_title(markdown: str) -> str:
    title = ""

    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            title = line.strip().split("# ", maxsplit=1)[1]

    return title

def markdown_to_html(markdown: str) -> tuple[str, str]:
    children: list[str] = []

    title = extract_title(markdown)

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node.to_html(2))

    content = "\n".join(children)

    return (title, content)