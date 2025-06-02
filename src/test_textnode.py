import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


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

    def test_split_nodes_delimiter(self):
        print()


if __name__ == "__main__":
    unittest.main()