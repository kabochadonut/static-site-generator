from textnode import TextNode, TextType
import re
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode

class BlockType(Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    UL = "ul"
    OL = "ol"
    LI = "li"
    QUOTE = "blockquote"
    CODE = "code"
    P = "p"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result_node_list: list[TextNode] = []
    for old in old_nodes:
        if old.text_type == TextType.CODE:
            result_node_list.append(old)
            continue
        if old.text == "":
            continue
        dl_next = old.text.startswith(delimiter)
        substrs = old.text.split(delimiter)
        for s in substrs:
            if s == "":
                continue
            if dl_next:
                result_node_list.append(TextNode(s, text_type))
            else:
                result_node_list.append(TextNode(s, old.text_type))
            dl_next = not dl_next
    return result_node_list

def extract_markdown_images(text) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result_node_list: list[TextNode] = []
    for old in old_nodes:
        images = extract_markdown_images(old.text)
        original_text = old.text
        for image_alt, image_link in images:
            temp, original_text = original_text.split(f"![{image_alt}]({image_link})", 1)
            if temp == "":
                result_node_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
            else:
                result_node_list.append(TextNode(temp, old.text_type, old.url))
                result_node_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
        if original_text != "":
            result_node_list.append(TextNode(original_text, old.text_type, old.url))
    return result_node_list



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result_node_list: list[TextNode] = []
    for old in old_nodes:
        links = extract_markdown_links(old.text)
        original_text = old.text
        for alt, link in links:
            temp, original_text = original_text.split(f"[{alt}]({link})", 1)
            if temp == "":
                result_node_list.append(TextNode(alt, TextType.LINK, link))
            else:
                result_node_list.append(TextNode(temp, old.text_type, old.url))
                result_node_list.append(TextNode(alt, TextType.LINK, link))
        if original_text != "":
                result_node_list.append(TextNode(original_text, old.text_type, old.url))
    return result_node_list

def text_to_textnodes(text) -> list[Textnode]:
    node_list = [TextNode(text, TextType.PLAIN)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    
    return node_list

def markdown_to_blocks(md: str) -> list[str]:
    blocks = md.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if block != "":
            result.append(block)
    return result

def block_to_blocktype(md_block: str) -> BlockType:
    heading_check = re.search(r"^#{1,} ", md_block)
    if heading_check != None:
        return string_to_heading(heading_check.group())
    if md_block.startswith("```\n"):
        return BlockType.CODE
    quote_check = re.search(r"^[^>]", md_block, re.M)
    if quote_check == None:
        return BlockType.QUOTE
    ul_check = re.search(r"^(?!- ).*$", md_block, re.M)
    if ul_check == None:
        return BlockType.UL
    ol_check = re.search(r"^(?!\d+\. ).*$", md_block, re.M)
    if ol_check == None:
        return BlockType.OL
    return BlockType.P

def string_to_heading(heading: str) -> BlockType:
    index = 0
    for i in range(0,6):
        if heading[i] == "#":
            index = i + 1
        else:
            break
    match index:
        case 1:
            return BlockType.H1
        case 2:
            return BlockType.H2
        case 3:
            return BlockType.H3       
        case 4:
            return BlockType.H4
        case 5:
            return BlockType.H5
        case 6:
            return BlockType.H6
        case _:
            raise Exception(f"Heading Index: Invalid index '{index}'")

def markdown_to_html(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    blocktypes = [block_to_blocktype(block) for block in blocks]
    nodes: list[HTMLNode] = []
    for i in range(len(blocks)):
        nodes.append(block_to_htmlnode(blocks[i], blocktypes[i]))
    return ParentNode("div", nodes)


def block_to_htmlnode(block: str, blocktype: BlockType, props: dict[str, str] | None = None) -> HTMLNode:
    match blocktype:
        case BlockType.UL | BlockType.OL:
            return list_block_to_htmlnode(block, blocktype)
        case BlockType.QUOTE:
            return quote_block_to_htmlnode(block)
        case BlockType.CODE:
            return code_block_to_htmlnode(block)
        case BlockType.H1 | BlockType.H2 | BlockType.H3 | BlockType.H4 | BlockType.H5 | BlockType.H6:
            return header_block_to_htmlnode(block, blocktype)
    textnodes = text_to_textnodes(block)
    child_nodes: list[LeafNode] = []
    for node in textnodes:
        child_nodes.append(node.text_node_to_html_node())
    return ParentNode(blocktype.value, child_nodes, props)

def list_block_to_htmlnode(block: str, blocktype: BlockType) -> HTMLNode:
    lines = block.split("\n")
    children: list[ParentNode] = []
    for line in lines:
        if blocktype == BlockType.UL:
            line = line.lstrip("- ")
        elif blocktype == BlockType.QUOTE:
            line = line.lstrip("> ")
        elif blocktype == BlockType.OL:
            line = line.lstrip(re.search(r"(^\d+\.\s+)", line).group())
        textnodes = text_to_textnodes(line)
        leafnodes = []
        for node in textnodes:
            leafnodes.append(node.text_node_to_html_node())
        children.append(ParentNode(BlockType.LI.value, leafnodes))
    return ParentNode(blocktype.value, children)

def quote_block_to_htmlnode(block: str) -> HTMLNode:
    lines = block.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].strip("> ")
    joined = "\n".join(lines)
    textnodes = text_to_textnodes(joined)
    children: list[LeafNode] = []
    for node in textnodes:
        children.append(node.text_node_to_html_node())
    return ParentNode(BlockType.QUOTE.value, children)

def code_block_to_htmlnode(block: str):
    child = LeafNode(BlockType.CODE.value, block.strip("`\n"))
    return ParentNode("pre", [child])

def header_block_to_htmlnode(block:str, blocktype: BlockType) -> HTMLNode:
    textnodes = text_to_textnodes(block.lstrip("# "))
    leafnodes = []
    for node in textnodes:
        leafnodes.append(node.text_node_to_html_node())
    return ParentNode(blocktype.value, leafnodes)

