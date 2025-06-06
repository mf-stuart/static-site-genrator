import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html_p(self):
        node = LeafNode("p", "Hello world!", None)
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")

    def test_to_html_a(self):
        node = LeafNode("a", "Hello world!", {"href": "www.google.com"})
        print(node.to_html())
        self.assertEqual(node.to_html(), "<a href=\"www.google.com\">Hello world!</a>")


    def test___repr__(self):
        node = LeafNode("p", "yo yo yo", None, )
        print(repr(node))


if __name__ == "__main__":
    unittest.main()
