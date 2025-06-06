import os
import re
import inline_markdown
import block_markdown
from block_markdown import BlockType
from parentnode import ParentNode
import textnode
from textnode import TextNode, TextType

def generate_pages_recursive(content_dir, template_dir, dst_dir, basepath):
    for fn in os.listdir(content_dir):
        if os.path.isdir(os.path.join(content_dir, fn)):
            generate_pages_recursive(os.path.join(content_dir, fn), template_dir, os.path.join(dst_dir, fn), basepath)
        else:
            destination_file = fn.replace(".md", ".html")
            generate_page(os.path.join(content_dir, fn), template_dir, os.path.join(dst_dir, destination_file), basepath)



def generate_page(src, template_path, dst, basepath):
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)
    print(f"Generating page from {src} to {dst} using {template_path}")

    with open(src, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    content_html_node = markdown_to_html_node(content)
    content_html_string = content_html_node.to_html()
    page_title = extract_title(content)

    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", content_html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)

    with open(dst, "w") as f:
        f.write(template)
        print(f"Wrote to {dst}")

def extract_title(markdown):
        captured = re.search(r"(?<=^# ).+(?=\n|$)", markdown, re.MULTILINE)
        if not captured:
            raise ValueError("invalid markdown, not h1 found")
        else:
            return captured.group().strip()

def markdown_to_html_node(markdown_string):
    root = ParentNode("div", [])
    blocks = block_markdown.markdown_to_blocks(markdown_string)
    for block in blocks:
        if block:
            root.children.append(block_text_to_children(block))
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



