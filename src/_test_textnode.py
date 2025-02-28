import unittest
from textnode import TextNode, TextType

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