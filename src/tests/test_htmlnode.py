import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode("p", "yo yo yo", None,
                        {
                            "href": "https://www.google.com",
                            "target": "_blank", }
                        )
        self.assertEqual(node.props_to_html(), ' '.join(f'{k}="{v}"' for k, v in node.props.items()))

    def test_props_to_html2(self):
        node = HTMLNode("p", "yo yo yo", None,
                        {
                            "href": "website.com",
                            "target": "_null", }
                        )
        self.assertEqual(node.props_to_html(), ' '.join(f'{k}="{v}"' for k, v in node.props.items()))

    def test___repr__(self):
        node = HTMLNode("p", "yo yo yo", None, )
        print(repr(node))


if __name__ == "__main__":
    unittest.main()
