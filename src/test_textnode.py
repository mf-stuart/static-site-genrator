import unittest
from textnode import (TextNode, TextType, text_node_to_html_node,
                      split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
                      split_nodes_image, split_nodes_link)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not  a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_str(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node), "TextNode(This is a text node, bold, None)")

    def test_neq_many(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is not  a text node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_t(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_a(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        print(split_nodes_delimiter([node], "`", TextType.CODE))
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE),
                         [TextNode("This is text with a " , TextType.TEXT),
                          TextNode("code block", TextType.CODE),
                         TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        print(split_nodes_delimiter([node], "_", TextType.ITALIC))
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC),
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("italic", TextType.ITALIC),
                          TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_mix(self):
        node = TextNode("This is text with _italic_ and **bold** words", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "_", TextType.ITALIC)
        second_pass = split_nodes_delimiter(first_pass, "**", TextType.BOLD)
        print(second_pass)
        self.assertEqual(second_pass,
                         [
                             TextNode("This is text with ", TextType.TEXT),
                             TextNode("italic", TextType.ITALIC),
                             TextNode(" and ", TextType.TEXT),
                             TextNode("bold", TextType.BOLD),
                             TextNode(" words", TextType.TEXT),
                         ])

    def test_split_nodes_delimiter_single(self):
        node = TextNode("**bold**", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
                         [TextNode("bold", TextType.BOLD),])

    def test_split_nodes_delimiter_multi(self):
        node = TextNode("**bold**_italic_", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "_", TextType.ITALIC)
        second_pass = split_nodes_delimiter(first_pass, "**", TextType.BOLD)
        self.assertEqual(second_pass,
                         [
                             TextNode("bold", TextType.BOLD),
                             TextNode("italic", TextType.ITALIC)
                         ])

    def test_split_nodes_delimiter_many_nodes(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a **bold text** node", TextType.TEXT)
        node3 = TextNode("This is another node", TextType.TEXT)
        node4 = TextNode("This is a _italic text_ node", TextType.TEXT)
        node5 = TextNode("This is a _italic_ and **bold** node", TextType.TEXT)

        old_nodes = [node1, node2, node3, node4, node5]
        firstpass = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        secondpass = split_nodes_delimiter(firstpass, "_", TextType.ITALIC)

        self.assertListEqual(
            secondpass,
            [TextNode("This is a text node", TextType.TEXT, None),
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
            TextNode(" node", TextType.TEXT, None)]
            )


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_image(self):
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with [google](https://google.com) and [youtube](https://www.youtube.com)]!",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("google", TextType.TEXT, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("youtube", TextType.TEXT, "https://www.youtube.com/@google"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()