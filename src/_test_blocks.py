import unittest

from blocks import markdown_to_blocks

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self) -> None:
        test_markdown = "I'm a block\n\nI'm a second block\nwith a second line\n\n\nI'm the last block\n"

        self.assertEqual(markdown_to_blocks(test_markdown), [
            "I'm a block",
            "I'm a second block\nwith a second line",
            "I'm the last block"
        ])
