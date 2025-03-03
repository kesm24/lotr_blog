# def main(hello: str) -> str:
#     print(hello)
#     return hello

# main("Hello World")

def extract_title(markdown: str) -> str:
    title = ""

    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            title = line.strip().split("# ", maxsplit=1)[1]

    return title