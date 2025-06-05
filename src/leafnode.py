from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("no tag value present")
        if self.tag is None:
            return self.value
        return (f'<{self.tag}'
                f'{(" " + " ".join(f"{k}=\"{v}\"" for k,v in self.props.items())) if self.props is not None else ""}>'
                f'{self.value}</{self.tag}>')

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"