import unittest
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ],
            split_nodes_delimiter([node], "`", TextType.CODE)
        )


    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ],
            split_nodes_delimiter([node], "_", TextType.ITALIC)
        )


    def test_split_nodes_delimiter_mix(self):
        node = TextNode("This is text with _italic_ and **bold** words", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "_", TextType.ITALIC)
        second_pass = split_nodes_delimiter(first_pass, "**", TextType.BOLD)
        self.assertListEqual([
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT)
        ],
            second_pass
        )


    def test_split_nodes_delimiter_single(self):
        node = TextNode("**bold**", TextType.TEXT)
        self.assertListEqual([
            TextNode("bold", TextType.BOLD)
        ],
            split_nodes_delimiter([node], "**", TextType.BOLD)
        )


    def test_split_nodes_delimiter_multi(self):
        node = TextNode("**bold**_italic_", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "_", TextType.ITALIC)
        second_pass = split_nodes_delimiter(first_pass, "**", TextType.BOLD)
        self.assertListEqual([
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC)
        ],
            second_pass
        )


    def test_split_nodes_delimiter_many_nodes(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a **bold text** node", TextType.TEXT)
        node3 = TextNode("This is another node", TextType.TEXT)
        node4 = TextNode("This is a _italic text_ node", TextType.TEXT)
        node5 = TextNode("This is a _italic_ and **bold** node", TextType.TEXT)

        old_nodes = [node1, node2, node3, node4, node5]
        firstpass = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        secondpass = split_nodes_delimiter(firstpass, "_", TextType.ITALIC)

        self.assertListEqual([
            TextNode("This is a text node", TextType.TEXT, None),
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("bold text", TextType.BOLD, None),
            TextNode(" node", TextType.TEXT, None),
            TextNode("This is another node", TextType.TEXT, None),
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("italic text", TextType.ITALIC, None),
            TextNode(" node", TextType.TEXT, None),
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" node", TextType.TEXT, None)
        ],
            secondpass
        )


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            extract_markdown_images(text)
        )


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            extract_markdown_links(text)
        )


    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
            new_nodes
        )


    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with [google](https://google.com) and [youtube](https://www.youtube.com)!",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with ", TextType.TEXT),
            TextNode("google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
            TextNode("!", TextType.TEXT),
        ],
            new_nodes
        )


    def test_split_nodes_all(self):
        node1 = TextNode("![test image](www.imagetest.com) is an image, but also some **bold** text", TextType.TEXT)
        node2 = TextNode("and here [test link](www.testlink.com) is an _italic_ link", TextType.TEXT)

        nodes = [node1, node2]
        full_pass = split_nodes_link(
            split_nodes_delimiter(
                split_nodes_image(
                    split_nodes_delimiter(nodes, "**", TextType.BOLD)
                ),
                "_", TextType.ITALIC
            )
        )

        self.assertListEqual([
            TextNode("test image", TextType.IMAGE, "www.imagetest.com"),
            TextNode(" is an image, but also some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("and here ", TextType.TEXT),
            TextNode("test link", TextType.LINK, "www.testlink.com"),
            TextNode(" is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" link", TextType.TEXT),
        ],
            full_pass
        )


    def test_text_to_textnodes(self):
        text = (
            "This is a **bold** and _italic_ text with `code` and a [link](https://example.com) "
            "and an image ![alt text](https://image.url/img.png)"
        )
        result = text_to_textnodes(text)

        self.assertListEqual([
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text with ", TextType.TEXT, None),
            TextNode("code", TextType.CODE, None),
            TextNode(" and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and an image ", TextType.TEXT, None),
            TextNode("alt text", TextType.IMAGE, "https://image.url/img.png"),
        ],
            result
        )

