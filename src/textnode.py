from enum import Enum
from leafnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None) :
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other) :
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self) :
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Unknown text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        text_slices = old_node.text.split(delimiter)
        for i, text_slice in enumerate(text_slices):
            if text_slice:
                new_nodes.append(TextNode(text_slice, old_node.text_type if i % 2 == 0 else text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    image_delimiter =r"(!\[[^\[\]]*\]\([^\(\)]*\))"
    for node in old_nodes:
        text_slices = re.split(image_delimiter, node.text)
        for text_slice in text_slices:
            if text_slice:
                if props := extract_markdown_images(text_slice):
                    new_nodes.append(TextNode(props[0][0],
                                              TextType.IMAGE,
                                              props[0][1]))
                else:
                    new_nodes.append(TextNode(text_slice, node.text_type))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    link_delimiter = r"(\[[^\[\]]*\]\([^\(\)]*\))"
    for node in old_nodes:
        text_slices = re.split(link_delimiter, node.text)
        for text_slice in text_slices:
            if text_slice:
                if props := extract_markdown_links(text_slice):
                    new_nodes.append(TextNode(props[0][0],
                                              TextType.IMAGE,
                                              props[0][1]))
                else:
                    new_nodes.append(TextNode(text_slice, node.text_type))
            return new_nodes

def extract_markdown_images(text):
    image_mask =r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_mask, text)

def extract_markdown_links(text):
    link_mask = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_mask, text)


