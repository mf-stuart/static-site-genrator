import unittest
from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
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
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_single_block(self):
        text = "This is a single paragraph with no indentation."
        self.assertListEqual(
            ["This is a single paragraph with no indentation."],
            markdown_to_blocks(text)
        )

    def test_multiple_blocks(self):
        text = "First block.\n\nSecond block.\n\nThird block."
        self.assertListEqual(
            ["First block.", "Second block.", "Third block."],
            markdown_to_blocks(text)
        )

    def test_indented_lines(self):
        text = "First line\n    Second line\n\tThird line\n\nNew block"
        self.assertListEqual(
            ["First line\nSecond line\nThird line", "New block"],
            markdown_to_blocks(text)
        )

    def test_edge_case_empty_blocks(self):
        text = "\n\n\n\nBlock after empty lines\n\nAnother block"
        self.assertListEqual(
            ["Block after empty lines", "Another block"],
            markdown_to_blocks(text)
        )

    def test_block_with_mixed_indentation(self):
        text = "Line 1\n  Line 2\n\tLine 3\n    Line 4\n\nNext block"
        self.assertListEqual(
            ["Line 1\nLine 2\nLine 3\nLine 4", "Next block"],
            markdown_to_blocks(text)
        )

    def test_block_to_blocktype_p(self):
        block ="This is a paragraph block."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_h1(self):
        block = "# This is a h1 block."
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_h2(self):
        block = "## This is a h2 block."
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_h3(self):
        block = "### This is a h3 block."
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_h4(self):
        block = "#### This is a h4 block."
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_h5(self):
        block = "##### This is a h5 block."
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_h6(self):
        block = "###### This is a h6 block."
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_hfail(self):
        block = "######This isnt a h6 block."
        self.assertNotEqual(BlockType.HEADING, block_to_block_type(block))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_c(self):
        block = "```This is a code block.\nAnother line\nAnd Another```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_block_to_blocktype_q(self):
        block = ">This is a quote block."
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_to_blocktype_ul(self):
        block = "- This is a ul block.\n- part 2\n- part 3"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_block_to_blocktype_failul(self):
        block = "- This is a ul block.\n-oops not anymore\n- wont work"
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_block_to_blocktype_ol(self):
        block = "1. This is a ol block.\n2. part 2\n3. part 3"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_to_blocktype_failol_nonnum(self):
        block = "1. This is a ol block.\nt. oops not anymore\n3. part 3"
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(block))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_failol_wspace(self):
        block = "1. This is a ol block.\n2.oops not anymore\n3. wont work"
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(block))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

if __name__ == "__main__":
    unittest.main()




