import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self) -> None:
        tag = "p"
        props = { "style": "color: black;" }

        test_node1 = HTMLNode(tag, props)

        self.assertEqual(test_node1.tag, tag)
        self.assertEqual(test_node1.props, props)

        test_node2 = HTMLNode()

        self.assertEqual(test_node2.tag, None)
        self.assertEqual(test_node2.props, None)

    def test_htmlnode_repr(self) -> None:
        tag = "p"
        props = { "style": "color: black;" }

        test_node = HTMLNode(tag, props)

        self.assertEqual(repr(test_node), "HTMLNode(p, {'style': 'color: black;'})")

    def test_htmlnode_eq(self) -> None:
        tag = "p"

        test_nodeA = HTMLNode(tag)
        test_nodeB = HTMLNode(tag)
        test_nodeC = HTMLNode()

        self.assertEqual(test_nodeA, test_nodeB)
        self.assertNotEqual(test_nodeA, test_nodeC)

    def test_htmlnode_to_html(self) -> None:
        test_node = HTMLNode()

        self.assertRaises(NotImplementedError, test_node.to_html)

    def test_htmlnode_props_to_html(self) -> None:
        test_node = HTMLNode("p", { "style": "color: black;" })

        self.assertEqual(test_node.props_to_html(), ' style="color: black;"')

class TestLeafNode(unittest.TestCase):
    def test_leafnode(self) -> None:
        tag = "p"
        value = "I'm a paragraph"
        props = { "style": "color: black;" }

        test_node = LeafNode(tag, value, props)

        self.assertEqual(test_node.tag, tag)
        self.assertEqual(test_node.value, value)
        self.assertEqual(test_node.props, props)

    def test_leafnode_repr(self) -> None:
        tag = "p"
        value = "I'm a paragraph"
        props = { "style": "color: black;" }

        test_node = LeafNode(tag, value, props)

        self.assertEqual(repr(test_node), f"LeafNode({tag}, {value}, {props})")

    def test_leafnode_eq(self) -> None:
        tag = "p"
        value = "I'm a paragraph"
        props = { "style": "color: black;" }

        test_nodeA = LeafNode(tag, value, props)
        test_nodeB = LeafNode(tag, value, props)
        test_nodeC = LeafNode(None, value)

        self.assertEqual(test_nodeA, test_nodeB)
        self.assertNotEqual(test_nodeA, test_nodeC)

    def test_leafnode_to_html(self) -> None:
        tag = "p"
        value = "I'm a paragraph"
        props = { "style": "color: black;" }

        test_node = LeafNode(tag, value, props)

        self.assertEqual(test_node.to_html(), f"<{tag} style=\"color: black;\">{value}</{tag}>")