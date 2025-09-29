import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class testBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        block = """###### This is a header"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_code(self):
        block = """```This is a code block```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

    def test_quote(self):
        block = """>This is a quote block
> with one quote line
> and two quote lines
> and three quote lines"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        block = """- This is a unordered list block
- with one line
- and two lines
- and three lines"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.UL
        )

    def test_ordered_list(self):
        block = """1. This is a unordered list block
2. with one line
3. and two lines
4. and three lines"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.OL
        )


if __name__ == "__main__":
    unittest.main()
