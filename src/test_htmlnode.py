import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        print("Testing HTMLNode")
        node = HTMLNode("h1", "yo", None, {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("h1", "yo", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("h1", "yo", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_children(self):
        child = HTMLNode("h1", "child", None, None)
        child2 = HTMLNode("h1", "child", None, None)
        node = HTMLNode("h1", "parent", [child], None)
        node2 = HTMLNode("h1", "parent", [child2], None)
        self.assertEqual(node, node2)
        # not sure this should be true but if different children have equal parameters, then they are equal in the parents children list

    
