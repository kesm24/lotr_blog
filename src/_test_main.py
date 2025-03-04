import os
import unittest

from main import copy_files, extract_title, markdown_to_html, remove_files

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

    def test_remove_files(self) -> None:
        if not os.path.exists("test_dest"):
            os.mkdir("test_dest")
            os.mkdir("test_dest/test_dir")

        f1 = open("test_dest/test_file1", "w")
        f1.write("testing")
        f1.close()

        f2 = open("test_dest/test_dir/test_file2", "w")
        f2.write("testing")
        f2.close()

        remove_files("test_dest")

        self.assertEqual(os.path.exists("public"), False)

    def test_copy_files(self) -> None:
        if not os.path.exists("test_src"):
            os.mkdir("test_src")
            os.mkdir("test_src/test_dir")

        f1 = open("test_src/test_file1", "w")
        f1.write("testing")
        f1.close()

        f2 = open("test_src/test_dir/test_file2", "w")
        f2.write("testing")
        f2.close()

        copy_files("test_src", "test_dest")

        self.assertTrue(os.path.isdir("test_dest"))
        self.assertTrue(os.path.exists("test_dest/test_file1"))
        test_file1 = open("test_dest/test_file1")
        self.assertEqual(test_file1.read(), "testing")
        self.assertTrue(os.path.isdir("test_dest/test_dir"))
        self.assertTrue(os.path.exists("test_dest/test_dir/test_file2"))
        test_file2 = open("test_dest/test_dir/test_file2")
        self.assertEqual(test_file2.read(), "testing")


        test_file1.close()
        test_file2.close()
        remove_files("test_src")
        remove_files("test_dest")