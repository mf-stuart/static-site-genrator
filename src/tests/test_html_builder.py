import unittest
from html_builder import markdown_to_html_node, extract_title

class TestHtmlBuilder(unittest.TestCase):

    def test_markdown_to_html_node_p(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
           "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            html
        )

    def test_markdown_to_html_node_c(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            html
        )

    def test_markdown_to_html_node_ul(self):
        md = """
            - hi
            - hello
            - world
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ul><li>hi</li><li>hello</li><li>world</li></ul></div>",
            html
        )
    def test_markdown_to_html_node_ol(self):
        md = """
        1. hi
        2. hello
        3. world
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ol><li>hi</li><li>hello</li><li>world</li></ol></div>",
            html
        )

    def test_inline_code_special_chars(self):
        md = "Use the `print(\"hello\")` function."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><p>Use the <code>print(\"hello\")</code> function.</p></div>",
            html
        )

    def test_extract_title(self):
        md = "# Hello World"
        self.assertEqual("Hello World!", extract_title(md))

    def test_extract_title_empty(self):
        md = ""
        self.assertRaises(ValueError, extract_title, md)



