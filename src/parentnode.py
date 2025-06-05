from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag present")
        if self.children is None:
            raise ValueError("no children present")
        return "".join(f"<{self.tag}>{"".join([child.to_html() for child in self.children])}</{self.tag}>" )
