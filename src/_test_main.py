import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self) -> None:
        test_markdown = """
            # I'm a title

            I'm a paragraph
        """

        title = extract_title(test_markdown)

        self.assertEqual(title, "I'm a title")