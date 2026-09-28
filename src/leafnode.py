from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
       super().__init__(tag, value, None, props) 

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError(f"{self}: Node value cannot be empty")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def props_to_html(self) -> str:
        return super().props_to_html()

    def __eq__(self, other: HTMLNode) -> bool:
        return self.tag == other.tag and self.value == other.value  and self.props == other.props

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

