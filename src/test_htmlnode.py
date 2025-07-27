import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        testprops = {}
        testprops["href"] = "https://www.google.com"
        testprops["target"]= "_blank"

        node = HTMLNode(props=testprops)
        result = node.props_to_html()
        test = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(result, test)

    def test_prop(self):
        testprops = {}
        testprops["href"] = "shineyhiney.com"

        node = HTMLNode(props=testprops)
        result = node.props_to_html()
        test = 'href="shineyhiney.com"'
        self.assertEqual(result, test)

    def test_prop(self):
        testprops = {}
        testprops["href"] = "https://www.koolkats.com"
        testprops["target"]= "_top"

        node = HTMLNode(props=testprops)
        result = node.props_to_html()
        test = 'href="https://www.koolkats.com" target="_top"'
        self.assertEqual(result, test)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), "Click me!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

if __name__ == "__main__":
    unittest.main()