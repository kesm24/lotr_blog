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
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
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
            if isinstance(child, ParentNode):
                html_str += f"\n"
                html_str += f"{child.to_html(indent + 1)}"
            else:
                html_str += f"{child.to_html()}"

        if isinstance(self.children[0], ParentNode):
            html_str += f"\n{indent_str}"

        html_str += f"</{self.tag}>"

        return html_str

