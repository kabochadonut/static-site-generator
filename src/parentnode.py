from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str,str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError(f"{self}: ParentNode tag cannot be empty or None")
        if not self.children:
            raise ValueError(f"{self}: ParentNode children cannot be empty or None")
        result = ""
        for child in self.children:
            result += child.to_html()
        if self.tag == "code":
            return f"<pre>{self.tag}{self.props_to_html()}>{self.value}</{self.tag}></pre>"
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"

    def props_to_html(self) -> str:
        return super().props_to_html()

