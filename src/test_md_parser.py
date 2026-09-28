import unittest
from md_parser import *
import re
from textnode import TextNode, TextType

class TestMDParser(unittest.TestCase):
    def test_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        eq_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, eq_nodes)

    def test_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        eq_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, eq_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with a ![banger pic](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with some trailing text",
            TextType.PLAIN,
        )
        node2 = TextNode(
            "![banger pic](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with some trailing text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.PLAIN, None), TextNode("banger pic", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.PLAIN, None), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"), TextNode(" with some trailing text", TextType.PLAIN, None), TextNode("banger pic", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.PLAIN, None), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"), TextNode(" with some trailing text", TextType.PLAIN, None)])

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This is text with a link ", TextType.PLAIN, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.PLAIN, None), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])
        node2 = TextNode(
            "leading [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), trailing",
            TextType.PLAIN,
        )
        new_nodes2 = split_nodes_link([node2])
        self.assertEqual(new_nodes2, [TextNode("leading ", TextType.PLAIN, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.PLAIN, None), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), TextNode(", trailing", TextType.PLAIN, None)])

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an [link](https://boot.dev) and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(text_to_textnodes(text), [TextNode("This is ", TextType.PLAIN, None), TextNode("text", TextType.BOLD, None), TextNode(" with an ", TextType.PLAIN, None), TextNode("italic", TextType.ITALIC, None), TextNode(" word and a ", TextType.PLAIN, None), TextNode("code block", TextType.CODE, None), TextNode(" and an ", TextType.PLAIN, None), TextNode("link", TextType.LINK, "https://boot.dev"), TextNode(" and a ", TextType.PLAIN, None), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])

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

    def test_md_to_blocktype_quote(self):
        text = """
> yo
>yo
>

"""
        block_type = block_to_blocktype(text.strip())
        self.assertEqual(block_type, BlockType.QUOTE)
        #print(f"BlockType: '{block_type}'")
        #quote_check = re.search(r"^[^>]", text.strip(), re.M)
        #if quote_check != None:
            #print(f"regex: '{quote_check.group()}'")

    def test_md_to_blocktype_heading(self):
        text = "## YO"
        text2 = " YO"
        #heading_check = re.search(r"^#{1,} ", text)
        #heading_check2 = re.search(r"^#{1,} ", text2)
        heading_check = block_to_blocktype(text.strip())
        heading_check2 = block_to_blocktype(text2.strip())
        self.assertEqual(heading_check, BlockType.H2)
        self.assertEqual(heading_check2, BlockType.P)

    def test_md_to_blocktype_code(self):
        text = """
```
code.block
```
"""
        block_type = block_to_blocktype(text.strip())
        self.assertEqual(block_type, BlockType.CODE)

    def test_md_to_blocktype_ul(self):
        text = """
- yo
- b
- ha
"""
        block_type = block_to_blocktype(text.strip())
        self.assertEqual(block_type, BlockType.UL)

    def test_md_to_blocktype_ol(self):
        text = """
1. yo
2. sl
4. sb
"""
        block_type = block_to_blocktype(text.strip())
        self.assertEqual(block_type, BlockType.OL)

    def test_md_to_blocktype_p(self):
        text = "hello, world"
        block_type = block_to_blocktype(text.strip())
        self.assertEqual(block_type, BlockType.P)

    def test_markdown_to_html(self):
        md = """
```
cheeky lil code block
**checking for delimiting**
_this should all be one string_
```

### YO YO

> this is a quote
>from your mum

1. something
2. somthin
3. sf;ad

- hello
- ajosd
- kill me

This is another paragraph with _italic_ text and `code` here

"""
        print(markdown_to_html(md).to_html())
