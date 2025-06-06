import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    LIST_ITEM = "list_item"

NESTED_TAGS = {
    BlockType.UNORDERED_LIST,
    BlockType.ORDERED_LIST,
    BlockType.CODE,
}

def markdown_to_blocks(text):
    block_strings = []
    raw_blocks = text.split("\n\n")
    for rb in raw_blocks:
        if rb:
            text = re.sub(r"(\n[\t ]+)", "\n", rb.strip())
            block_strings.append(text)
    return block_strings

def block_to_block_type(block):

    match block:
        case str() if re.match(r"^#{1,6} ", block):
            return BlockType.HEADING
        case str() if re.match(r"^`{3}[\s\S]*`{3}$", block):
            return BlockType.CODE
        case str() if re.match(r"^>", block):
            return BlockType.QUOTE
        case str() if re.fullmatch(r"^(?:- .*\n)*- .*$", block, re.MULTILINE):
            return BlockType.UNORDERED_LIST
        case str() if re.fullmatch(r"^(?:\d+\. .*\n)*\d+\. .*$", block, re.MULTILINE):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

def block_type_to_tag(block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "q"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
        case BlockType.LIST_ITEM:
            return "li"
        case BlockType.HEADING:
            raise ValueError("unsupported block type, use heading_block_to_tag()")
        case _:
            return "p"

def heading_block_to_tag(block):
    return f"h{re.match(r'^#{1,6} ', block).group().count('#')}"

def block_to_type_and_tag(block):
    block_type = block_to_block_type(block)
    try:
        tag = block_type_to_tag(block_type)
    except ValueError:
        tag = heading_block_to_tag(block)
    return block_type, tag

def nested_block_type_to_outer_inner_tags(block_type):
    match block_type:
        case BlockType.UNORDERED_LIST:
            return ("ul", "li")
        case BlockType.ORDERED_LIST:
            return ("ol", "li")
        case BlockType.CODE:
            return ("pre", "code")
        case _:
            raise ValueError("block type is not a nested tag")

def trim_text(text):
    match block_to_block_type(text):
        case BlockType.HEADING:
            return re.sub(r"^#{1,6} ", "", text, flags=re.MULTILINE)
        case BlockType.QUOTE:
            return re.sub(r"^>", "", text, flags=re.MULTILINE)
        case BlockType.UNORDERED_LIST:
            return re.sub(r"^- ", "", text, flags=re.MULTILINE)
        case BlockType.ORDERED_LIST:
            return re.sub(r"^\d+\. ", "", text, flags=re.MULTILINE)
        case BlockType.CODE:
            return re.sub(r"(`{3}\s?)", "", text)
        case BlockType.PARAGRAPH:
            return re.sub(r"\n", " ", text)
        case _:
            return text

def is_nested_block_type(block_type):
    if block_type in NESTED_TAGS:
        return True
    return False

