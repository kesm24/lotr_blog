from blocks import BlockType, split_block_to_lines
from textnode import TextNode, TextType, markdown_to_text_nodes

class HTMLNode:
    def __init__(self, tag: str | None = None, props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.props})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, HTMLNode) and
            self.tag == other.tag and
            self.props == other.props
        )

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props == None:
            return ""

        props_html = ""

        for (key, val) in self.props.items():
            props_html += f' {key}="{val}"'

        return props_html

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, props)
        self.value = value

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, LeafNode) and
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )

    def to_html(self) -> str:
        if self.tag == None:
            return f"{self.value}"

        if self.value == None:
            return f"<{self.tag}{self.props_to_html()} />"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["ParentNode | LeafNode"], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, props)
        self.children = children

    def __repr__(self) -> str:
        return self.__format_repr(self)

    def __format_repr(self, node: "ParentNode | LeafNode", indent: int = 0) -> str:
        repr_str = ""
        indent_str = ""

        for _ in range(0, indent):
            indent_str += "\t"

        if isinstance(node, LeafNode):
            return f"{indent_str}{repr(node)}"

        repr_str += f"{indent_str}ParentNode({node.tag}, ["

        for child in node.children:
            repr_str += "\n"
            repr_str += f"{self.__format_repr(child, indent + 1)}"
            if child != node.children[-1]:
                repr_str += ","

        if len(node.children) > 0:
            repr_str += "\n"

        repr_str += f"{indent_str}], {node.props})"

        return repr_str

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ParentNode) and
            self.tag == other.tag and
            self.children == other.children and
            self.props == other.props
        )

    def to_html(self, indent: int = 0) -> str:
        html_str = ""
        indent_str = ""

        for _ in range(0, indent):
            indent_str += "\t"

        html_str += f"{indent_str}<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            if isinstance(child, ParentNode) and self.tag != "pre":
                html_str += f"\n"
                html_str += f"{child.to_html(indent + 1)}"
            else:
                child_html = f"{child.to_html()}"

                if self.tag == "code":
                    if not child_html.strip().startswith("}") and not child_html.strip().endswith("{"):
                        child_html = child_html.replace("\n", "\n\t", 1)
                        child_html += "\n"
                    else:
                        child_html = child_html.strip()

                html_str += f"{child_html}"

        if isinstance(self.children[0], ParentNode) and self.tag != "pre":
            html_str += f"\n{indent_str}"

        html_str += f"</{self.tag}>"

        return html_str

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            assert isinstance(text_node.url, str)
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE:
            assert isinstance(text_node.url, str)
            return LeafNode("img", None, { "src": text_node.url, "alt": text_node.text })

def block_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    children: list[ParentNode | LeafNode] = []

    lines = split_block_to_lines(block, block_type)

    for line in lines:
        inner_children: list[ParentNode | LeafNode] = []

        if block_type == BlockType.CODE:
            line = "\n" + line

        text_nodes = markdown_to_text_nodes(line)

        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            inner_children.append(html_node)

        if block_type in [BlockType.U_LIST, BlockType.O_LIST]:
            list_node = ParentNode("li", inner_children)
            children.append(list_node)
        else:
            children.extend(inner_children)

    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", children)
        case BlockType.HEADING:
            level = len(block.strip().split(" ", maxsplit=1)[0])
            return ParentNode(f"h{level}", children)
        case BlockType.CODE:
            return ParentNode("pre", [
                ParentNode("code", children)
            ])
        case BlockType.QUOTE:
            return ParentNode("blockquote", children)
        case BlockType.U_LIST:
            return ParentNode("ul", children)
        case BlockType.O_LIST:
            return ParentNode("ol", children)