import unittest

from blocks import markdown_to_blocks, BlockType, block_to_block_type, split_block_to_lines

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self) -> None:
        test_markdown = "I'm a block\n\nI'm a second block\nwith a second line\n\n\nI'm the last block\n"

        self.assertEqual(markdown_to_blocks(test_markdown), [
            "I'm a block",
            "I'm a second block\nwith a second line",
            "I'm the last block"
        ])

    def test_block_to_block_type(self) -> None:
        paragraph_block = "I'm a paragraph block"
        heading_block1 = "# I'm a heading block"
        heading_block2= "### I'm a smaller heading block"
        heading_block3 = "###### I'm the smallest heading block"
        heading_block_invalid = "####### I'm an invalid heading block"
        code_block = "``` I'm a code block ```"
        quote_block = "> I'm a quote block"
        u_list_block = "- I'm an unordered list block"
        o_list_block = "1. I'm an ordered list block"

        self.assertEqual(block_to_block_type(paragraph_block), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(heading_block1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading_block2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading_block3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(heading_block_invalid), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(u_list_block), BlockType.U_LIST)
        self.assertEqual(block_to_block_type(o_list_block), BlockType.O_LIST)

    def test_split_block_to_lines(self) -> None:
        paragraph_block = "I'm a paragraph block\n\n with two lines\n\n"
        heading_block = "### I'm a heading block"
        code_block = "``` \nI'm a code block\n ```"
        quote_block = "> I'm a quote block"
        u_list_block = "* I'm an unordered list block\n * I'm still an unordered list block"
        o_list_block = "1. I'm an ordered list block\n 2. I'm still an ordered list block"

        self.assertEqual(split_block_to_lines(paragraph_block, BlockType.PARAGRAPH), [
            "I'm a paragraph block",
            "with two lines"
        ])
        self.assertEqual(split_block_to_lines(heading_block, BlockType.HEADING), ["I'm a heading block"])
        self.assertEqual(split_block_to_lines(code_block, BlockType.CODE), ["I'm a code block"])
        self.assertEqual(split_block_to_lines(quote_block, BlockType.QUOTE), ["I'm a quote block"])
        self.assertEqual(split_block_to_lines(u_list_block, BlockType.U_LIST), ["I'm an unordered list block", "I'm still an unordered list block"])
        self.assertEqual(split_block_to_lines(o_list_block, BlockType.O_LIST), ["I'm an ordered list block", "I'm still an ordered list block"])
