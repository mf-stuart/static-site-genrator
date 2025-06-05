import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    image_mask =r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_mask, text)

def extract_markdown_links(text):
    link_mask = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_mask, text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        text_slices = old_node.text.split(delimiter)
        for i, text_slice in enumerate(text_slices):
            if text_slice:
                args = (old_node.text_type, old_node.url) if i % 2 == 0 else (text_type, None)
                new_nodes.append(TextNode(text_slice, *args))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    image_delimiter =r"(!\[[^\[\]]*\]\([^\(\)]*\))"
    for node in old_nodes:
        text_slices = re.split(image_delimiter, node.text)
        for text_slice in text_slices:
            if text_slice:
                if props := extract_markdown_images(text_slice):
                    new_nodes.append(
                        TextNode(props[0][0], TextType.IMAGE, props[0][1]))
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
                    new_nodes.append(
                        TextNode(props[0][0], TextType.LINK, props[0][1]))
                else:
                    new_nodes.append(TextNode(text_slice, node.text_type, node.url))
    return new_nodes

def text_to_textnodes(text):
    root_node = TextNode(text, TextType.TEXT)
    return (
        split_nodes_link(
            split_nodes_image(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        split_nodes_delimiter([root_node], "_", TextType.ITALIC),
                     "**", TextType.BOLD),
                    "`", TextType.CODE)
            )
        )
    )