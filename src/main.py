import os
import shutil
import sys
from blocks import block_to_block_type, markdown_to_blocks
from htmlnode import block_to_html_node

def extract_title(markdown: str) -> str:
    title = ""

    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            title = line.strip().split("# ", maxsplit=1)[1]

    return title

def markdown_to_html(markdown: str, indent: int = 0) -> tuple[str, str]:
    children: list[str] = []

    title = extract_title(markdown)

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node.to_html(indent))

    content = "\n".join(children)

    return (title, f"\n{content}\n")

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

def generate_page(basepath: str, src: str, template: str, dest: str) -> None:
    print(f"Generating page from {src} to {dest} using {template}")

    if not os.path.exists(src):
        raise FileNotFoundError(f"content file '{src}' does not exist")

    if not os.path.isfile(src):
        raise IsADirectoryError(f"'{src}' is not a file")

    if os.path.splitext(src)[1] != ".md":
        raise ValueError(f"content file '{src}' is not a markdown file")

    if not os.path.exists(template):
        raise FileNotFoundError(f"template '{template}' does not exist")

    if os.path.splitext(template)[1] != ".html":
        raise ValueError(f"template file '{template}' is not an html file")

    if os.path.splitext(dest)[1] != ".html":
        raise ValueError(f"destination file '{dest}' must be an html file")

    src_file = open(src)
    src_contents = src_file.read()
    src_file.close()

    title, content = markdown_to_html(src_contents, 3)

    template_file = open(template)
    template_contents = template_file.read()
    template_file.close()

    dest_contents = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", content)

    if basepath == "./":
        basepath = "/"
    dest_contents = dest_contents.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    dest_file = open(dest, "w")
    dest_file.write(dest_contents)
    dest_file.close()

def generate_pages_recursive(basepath: str, src: str, template: str, dest: str) -> None:
    if not os.path.exists(src) or not os.path.isdir(src):
        raise NotADirectoryError(f"path '{src}' is not a valid directory")

    if not os.path.exists(template):
        raise FileNotFoundError(f"template file '{template}' does not exist")

    if os.path.splitext(template)[1] != ".html":
        raise ValueError(f"template file '{template}' is not an html file")

    if os.path.isfile(dest):
        raise IsADirectoryError(f"destination '{dest}' is not a directory")

    if not os.path.exists(dest):
        os.mkdir(dest)

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)
        if os.path.isdir(src_path):
            generate_pages_recursive(basepath, src_path, template, dest_path)
        else:
            _, ext = os.path.splitext(src_path)

            if ext == ".md":
                generate_page(basepath, src_path, template, dest_path.replace(ext, ".html"))

def main(basepath: str = "./") -> None:
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    content_path = os.path.join(basepath, "content")
    template_path = os.path.join(basepath, "template.html")
    static_path = os.path.join(basepath, "static")
    public_path = os.path.join(basepath, "docs")

    remove_files(public_path)
    copy_files(static_path, public_path)
    generate_pages_recursive(basepath, content_path, template_path, public_path)

main()