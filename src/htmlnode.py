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
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"