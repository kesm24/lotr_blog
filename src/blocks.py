from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "u_list"
    O_LIST = "o_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []

    for block in markdown.split("\n\n"):
        if block == "" or block == "\n":
            continue
        blocks.append(block.strip())

    return blocks

def block_to_block_type(block: str) -> BlockType:
    block_start = block.strip().split(maxsplit=1)[0].strip()

    if block_start in "######":
        return BlockType.HEADING
    if block_start == "```" and block.strip().endswith("```"):
        return BlockType.CODE
    if block_start == ">":
        return BlockType.QUOTE
    if block_start == "*" or block_start == "-":
        return BlockType.U_LIST
    if block_start == "1.":
        return BlockType.O_LIST

    return BlockType.PARAGRAPH