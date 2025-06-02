import unittest
from parentnode import ParentNode
from leafnode import LeafNode



class TestParentNode(unittest.TestCase):

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

    def test_to_html_with_no_children(self):
        node = ParentNode("span", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_neither(self):
        node = ParentNode(None, None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()