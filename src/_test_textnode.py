import unittest
from textnode import TextNode, TextType, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_textnode(self) -> None:
        text = "I'm a text node"
        text_type = TextType.TEXT
        test_node = TextNode(text, text_type)

        self.assertEqual(test_node.text, text)
        self.assertEqual(test_node.text_type, text_type)
        self.assertEqual(test_node.url, None)

    def test_textnode_repr(self) -> None:
        text = "I'm a text node"
        text_type = TextType.TEXT
        test_node = TextNode(text, text_type)

        self.assertEqual(repr(test_node), f"TextNode({text}, {text_type.value}, None)")

    def test_textnode_eq(self) -> None:
        text = "I'm a text node"
        text_type = TextType.TEXT

        test_nodeA = TextNode(text, text_type)
        test_nodeB = TextNode(text, text_type)
        test_nodeC = TextNode("I'm a **bold** node", TextType.BOLD)

        self.assertEqual(test_nodeA, test_nodeB)
        self.assertNotEqual(test_nodeA, test_nodeC)

class TestTextNodeUtils(unittest.TestCase):
    def test_split_nodes_delimiter(self) -> None:
        text_node = TextNode("I'm a text node", TextType.TEXT)
        bold_node = TextNode("I'm a **bold** node", TextType.TEXT)
        italic_node = TextNode("_I'm_ an italic node", TextType.TEXT)
        invalid_node = TextNode("I'm an **invalid node", TextType.TEXT)

        test_bold = split_nodes_delimiter([text_node, bold_node, italic_node], "**", TextType.BOLD)

        self.assertEqual(test_bold, [
            text_node,
            TextNode("I'm a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT),
            italic_node
        ])

        test_italic = split_nodes_delimiter(test_bold, "_", TextType.ITALIC)

        self.assertEqual(test_italic, [
            text_node,
            TextNode("I'm a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT),
            TextNode("I'm", TextType.ITALIC),
            TextNode(" an italic node", TextType.TEXT)
        ])

        self.assertRaises(ValueError, split_nodes_delimiter, [invalid_node], "**", TextType.BOLD)