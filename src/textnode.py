import re
from enum import Enum
from htmlnode import *

class TextType(Enum):
    LINK = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    IMAGE = 5
    TEXT = 6

class BlockType(Enum):
    P = 1
    H = 2
    C = 3
    Q = 4
    UL = 5
    OL = 6

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type ==  TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    if text_node.text_type ==  TextType.BOLD:
        return LeafNode("b", text_node.text, None)
    if text_node.text_type ==  TextType.ITALIC:
        return LeafNode("i", text_node.text, None)
    if text_node.text_type ==  TextType.CODE:
        return LeafNode("code", text_node.text, None)
    if text_node.text_type ==  TextType.LINK:
        props = {}
        props["href"] = text_node.url
        return LeafNode("a", text_node.text, props)
    if text_node.text_type ==  TextType.IMAGE:
        props = {}
        props["src"] = text_node.url
        props["alt"] = text_node.text
        return LeafNode("img", "", props)
    raise Exception(f"No, no, no. {text_node.text_type} no here.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text.count(delimiter) % 2 == 0:
                nodes_text = node.text.split(delimiter)
                for i in range(len(nodes_text)):
                    if nodes_text[i] != '':
                        if i % 2 != 0:
                            new_nodes.append(TextNode(nodes_text[i], text_type))
                        else:
                            new_nodes.append(TextNode(nodes_text[i], TextType.TEXT))
            else:
                raise Exception("invalid Markdown syntax")
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        if node.text_type != TextType.TEXT or not extract_markdown_images(node.text):
            new_nodes.append(node)
        else:
            image_data = extract_markdown_images(node.text)
            for data in image_data:
                alt_text = data[0]
                link = data[1]
        
                delimiter = f"![{alt_text}]({link})"
                sections = remaining_text.split(delimiter, 1)
                
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, link))

                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        if node.text_type != TextType.TEXT or not extract_markdown_links(node.text):
            new_nodes.append(node)
        else:
            link_data = extract_markdown_links(node.text)
            for data in link_data:
                alt_text = data[0]
                link = data[1]
        
                delimiter = f"[{alt_text}]({link})"
                sections = remaining_text.split(delimiter, 1)
                
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.LINK, link))

                remaining_text = sections[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    initial_node = [TextNode(text, TextType.TEXT)]
    
    split_image_nodes = split_nodes_image(initial_node)
    
    link_nodes = split_nodes_link(split_image_nodes)

    bold_nodes = split_nodes_delimiter(link_nodes, "**",TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_",TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`",TextType.CODE)

    return code_nodes

def markdown_to_blocks(markdown):
    raw_blocks = markdown.strip().split("\n\n")
    
    blocks = []
    for block in raw_blocks:
        cleaned_block = "\n".join(line.strip() for line in block.strip().splitlines())
        if cleaned_block:
            blocks.append(cleaned_block)
    
    return blocks

def block_to_block_type(block):

    # Check for heading
    if block.startswith("#"):
        block_type = BlockType.H

    #Check for code
    elif block.startswith("```") and block.endswith("```"):
        block_type = BlockType.C
    
    # Check for quote
    elif block.startswith(">"):
        block_type = BlockType.Q
    
    # Check for UL
    elif block.startswith("- "):
        block_type = BlockType.UL

    # Check for OL
    elif re.match(r'^\d+\.\s', block):
        block_type = BlockType.OL
    
    else:
        block_type = BlockType.P

    return block_type

def markdown_to_html_node(markdown):
    new_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.H:
            count = 0
            for char in block:
                if char == '#':
                    count += 1
                else:
                    break
            tag = f"h{count}"
            text = block[count:].strip()
            children = text_to_children(text)
            new_nodes.append(HTMLNode(tag, None, children))

        elif type == BlockType.P:
            tag = "p"
            # Replace newlines with spaces
            clean_text = block.replace('\n', ' ')
            children = text_to_children(clean_text)
            new_nodes.append(HTMLNode(tag, None, children))

        elif type == BlockType.Q:
            lines = block.split('\n')
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.lstrip('> '))
            text = '\n'.join(cleaned_lines)
            children = text_to_children(text)
            new_nodes.append(HTMLNode("blockquote", None, children))
        
        elif type == BlockType.OL:
            lines = block.split('\n')
            html = []
            for line in lines:
                space_index = line.find(' ')
                clean = line[space_index + 1:]
                children = text_to_children(clean)
                html.append(HTMLNode("li", None, children))
            new_nodes.append(HTMLNode("ol", None, html))

        elif type == BlockType.UL:
            lines = block.split('\n')
            html = []
            for line in lines:
                clean = line[2:]
                children = text_to_children(clean)
                html.append(HTMLNode("li", None, children))
            new_nodes.append(HTMLNode("ul", None, html))

        elif type == BlockType.C:
            clean = block.strip("```")
            if clean.startswith('\n'):
                clean = clean[1:]  # Remove the first newline
            tnode = TextNode(clean, TextType.TEXT)
            hnode = text_node_to_html_node(tnode)
            inner = HTMLNode("code", None, [hnode])
            outer = HTMLNode("pre", None, [inner])
            new_nodes.append(outer)


    return HTMLNode("div", None, new_nodes)

def text_to_children(text):
    tnodes = text_to_textnodes(text)
    html_nodes = []
    for node in tnodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes 
