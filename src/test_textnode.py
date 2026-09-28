import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("Testing TextNode")
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("yo", TextType.BOLD)
        node2 = TextNode("yo", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_url_default(self):
        node = TextNode("yo", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    

if __name__ == "__main__":
    unittest.main()
