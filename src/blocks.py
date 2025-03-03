def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []

    for block in markdown.split("\n\n"):
        if block == "" or block == "\n":
            continue
        blocks.append(block.strip())

    return blocks