import unittest

from main import extract_title, markdown_to_html

class TestMain(unittest.TestCase):
    def test_extract_title(self) -> None:
        test_markdown = """
            # I'm a title

            I'm a paragraph
        """

        title = extract_title(test_markdown)

        self.assertEqual(title, "I'm a title")

    def test_markdown_to_html(self) -> None:
        test_markdown = """
            # I'm a title

            I'm a paragraph

            * I'm an unordered list

            1. I'm an ordered list
        """

        (title, content) = markdown_to_html(test_markdown)

        self.assertEqual(title, "I'm a title")
        self.assertEqual(content,"\n\t\t".join([
            "\t\t<h1>I'm a title</h1>",
            "<p>I'm a paragraph</p>",
            "<ul>",
            "\t<li>I'm an unordered list</li>",
            "</ul>",
            "<ol>",
            "\t<li>I'm an ordered list</li>",
            "</ol>"
        ]))