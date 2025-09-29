
from htmlnode import ParentNode, LeafNode
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node 

def markdown_to_html_node(markdown):
    html_nodes_list = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:     
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                html_nodes_list.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                html_nodes_list.append(heading_to_html_node(block))
            case BlockType.CODE:
                raw = block.strip().removeprefix("```").removesuffix("```").lstrip("\n").rstrip("\n")
                html_nodes_list.append(ParentNode("pre", [LeafNode("code", raw + "\n")]))
            case BlockType.QUOTE:
                html_nodes_list.append(quote_to_html_node(block))
            case BlockType.UL:
                html_nodes_list.append(ul_to_html_node(block))
            case BlockType.OL:
                html_nodes_list.append(ol_to_html_node(block))
            case _:
                raise Exception("Invalid block type")
    return ParentNode("div", html_nodes_list)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_to_html_node(block):
    first = block.splitlines()[0]
    level = len(first) - len(first.lstrip("#"))
    level = max(1, min(6, level))
    content = first[level:].lstrip()
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)

def quote_to_html_node(block):
    clean = []
    for line in block.splitlines():
        clean.append(line.lstrip().removeprefix("> ").removeprefix(">"))
    content = " ".join(clean).strip()
    return ParentNode("blockquote", text_to_children(content))

def ul_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_line = line.lstrip("-").strip()
        children = text_to_children(new_line)
        new_lines.append(ParentNode("li", children))
    return ParentNode("ul", new_lines)

def ol_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_line = line[3:]
        children = text_to_children(new_line)
        new_lines.append(ParentNode("li", children))
    return ParentNode("ol", new_lines)
