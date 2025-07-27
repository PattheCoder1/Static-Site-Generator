import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        url_node = TextNode("This is a link", TextType.LINK, "www.amandaplease.com")
        url_node1 = TextNode("This is a link", TextType.LINK)
        self.assertNotEqual(url_node, url_node1)
    
    def test_type(self):
        type_node = TextNode("words blah blah", TextType.BOLD)
        type_node1 = TextNode("words blah blah", TextType.ITALIC)
        self.assertNotEqual(type_node, type_node1)

    def test_null(self):
        null_node = TextNode("", TextType.CODE)
        null_node1 = TextNode("yoyoyoyo", TextType.LINK, "yo.com")
        self.assertNotEqual(null_node, null_node1)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")

    def test_split(self):
        old_node = TextNode("This is text with *bold* text in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "*", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with ", TextType.TEXT),
                                     TextNode("bold",TextType.BOLD),
                                     TextNode(" text in it",TextType.TEXT)])

    def test_split(self):
        old_node = TextNode("This is text with _italic text_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with ", TextType.TEXT),
                                     TextNode("italic text",TextType.ITALIC),
                                     TextNode(" in it",TextType.TEXT)])
    
    def test_split(self):
        old_node = TextNode("This is text with _italic text_ in it", TextType.LINK)
        new_nodes = split_nodes_delimiter([old_node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with _italic text_ in it", TextType.LINK)])

    def test_split(self):
        old_node = [TextNode("This is text with _italic text_ in it", TextType.TEXT),
                    TextNode("This is text with _italic text_ in it", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_node, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with ", TextType.TEXT),
                                     TextNode("italic text",TextType.ITALIC),
                                     TextNode(" in it",TextType.TEXT),
                                     TextNode("This is text with ", TextType.TEXT),
                                     TextNode("italic text",TextType.ITALIC),
                                     TextNode(" in it",TextType.TEXT)])
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        " ![doin ya mom](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("doin ya mom", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_images(
        "visit ![Jon's](https://www.Jon.com) website"
        )
        self.assertListEqual([("Jon's", "https://www.Jon.com")], matches)
    

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com"
                ),
            ],
            new_nodes,
        )
    
    def test_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        test = text_to_textnodes(text)

        self.assertEqual([
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    ], test)
        
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type(self):
        block = "### Header here"
        self.assertEqual(
            BlockType.H,
            block_to_block_type(block)
        )

    def test_block_type(self):
        block = "``` Cool code shit ```"
        self.assertEqual(
            BlockType.C,
            block_to_block_type(block)
        )

    def test_block_type(self):
        block = "``` not real code"
        self.assertEqual(
            BlockType.P,
            block_to_block_type(block)
        )

    def test_block_type(self):
        block = "1. test\n2. test"
        self.assertEqual(
            BlockType.OL,
            block_to_block_type(block)
        )

    def test_block_type(self):
        block = "- testing unordered lists\n- anotha one"
        self.assertEqual(
            BlockType.UL,
            block_to_block_type(block)
        )

    def test_block_type(self):
        block = "> boot.dev is cool"
        self.assertEqual(
            BlockType.Q,
            block_to_block_type(block)
        )

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()