import os
import shutil
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

def remove_files(dest: str) -> None:
    if not os.path.exists(dest):
        return

    for file in os.listdir(dest):
        dest_path = os.path.join(dest, file)

        if os.path.isdir(dest_path):
           remove_files(dest_path)
        else:
           os.remove(dest_path)

    os.rmdir(dest)

def copy_files(src: str, dest: str) -> None:
    if not os.path.exists(src) or not os.path.isdir(src):
        raise NotADirectoryError(f"directory '{src}' does not exist")

    if not os.path.exists(dest):
        os.mkdir(dest)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)

        if os.path.isdir(src_path):
            copy_files(src_path, dest_path)
        else:
            shutil.copyfile(src_path, dest_path)