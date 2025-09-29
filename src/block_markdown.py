import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split(sep="\n\n")
    for i in range(0,len(blocks)):
        blocks[i] = blocks[i].strip("\n")

    blocks = list(filter(None,blocks))
    return blocks

def block_to_block_type(block):
    if block.startswith(("# ","## ", "### ","#### ", "##### ", "###### ")): return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"): return BlockType.CODE
    block_lines = block.split("\n")
    is_quote = True
    for line in block_lines:
        if not line[0] == ">": 
            is_quote = False
            break
    if is_quote: return BlockType.QUOTE

    is_unordered = True
    for line in block_lines:
        if not line.startswith("- "): 
            is_unordered = False
            break
    if is_unordered: return BlockType.UL

    is_ordered = True
    for i in range(0,len(block_lines)):
        if not block_lines[i].startswith(f"{i+1}. "): 
            is_ordered = False
            break
    
    if is_ordered: return BlockType.OL

    return BlockType.PARAGRAPH

