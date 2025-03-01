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

    def to_html(self) -> None:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props == None:
            return ""

        props_html = ""

        for (key, val) in self.props.items():
            props_html += f'{key}="{val}" '

        return props_html