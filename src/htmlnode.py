
class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props == None or self.props == "":
            return ""
        prop_list = []
        for key in self.props:
            prop_list.append(f' {key}="{self.props[key]}"')
        return "".join(prop_list)

    def __eq__(self, other: HTMLNode) -> bool:
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
