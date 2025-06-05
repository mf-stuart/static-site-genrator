import inline_markdown
import block_markdown
from block_markdown import BlockType
from parentnode import ParentNode
import textnode
from textnode import TextNode, TextType

def markdown_to_html_node(markdown_string):
    root = ParentNode("div", [])
    blocks = block_markdown.markdown_to_blocks(markdown_string)
    for block in blocks:
        if block:
            root.children.append(block_text_to_children(block))
    print(root.to_html())
    return root

def block_text_to_children(block):

    parent_block_type, parent_tag = block_markdown.block_to_type_and_tag(block)

    if parent_block_type is BlockType.CODE:
        parent_node = ParentNode("pre", [])
        trimmed_text = block_markdown.trim_text(block)
        code_node = TextNode(trimmed_text, TextType.CODE)
        html_node = textnode.text_node_to_html_node(code_node)
        parent_node.children.append(html_node)
        return parent_node

    elif block_markdown.is_nested_block_type(parent_block_type):
        out_tag, in_tag = block_markdown.nested_block_type_to_outer_inner_tags(parent_block_type)
        child_nodes = []
        parent_node = ParentNode(out_tag, child_nodes)
        for line in block_markdown.trim_text(block).split("\n"):
            if line:
                new_text_nodes = inline_markdown.text_to_textnodes(line)
                new_html_nodes = list(map(lambda n: textnode.text_node_to_html_node(n), new_text_nodes))
                child_nodes.append(ParentNode(in_tag, new_html_nodes))
        return parent_node

    else:
        parent_node = ParentNode(parent_tag, [])
        trimmed_text = block_markdown.trim_text(block)
        new_text_nodes = inline_markdown.text_to_textnodes(trimmed_text)
        new_html_nodes = list(map(lambda n: textnode.text_node_to_html_node(n), new_text_nodes))
        parent_node.children.extend(new_html_nodes)
        return parent_node



