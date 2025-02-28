import unittest
from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_images, split_nodes_links

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
    def test_extract_markdown_images(self) -> None:
        test_markdown1 = "I'm an ![image](image.jpeg)"

        images1 = extract_markdown_images(test_markdown1)
        alt1, url1 = images1[0]

        self.assertEqual(alt1, "image")
        self.assertEqual(url1, "image.jpeg")

        test_markdown2 = "I'm a ![second image](image2.jpeg)"

        images2 = extract_markdown_images(test_markdown2)
        alt2, url2 = images2[0]

        self.assertEqual(alt2, "second image")
        self.assertEqual(url2, "image2.jpeg")

        test_markdown2 = ""

        images3 = extract_markdown_images(test_markdown2)

        self.assertEqual(images3, [])

    def test_split_nodes_images(self) -> None:
        image_node1 = TextNode("I'm an ![image](image.jpeg)", TextType.TEXT)

        test_images1 = split_nodes_images([image_node1])

        self.assertEqual(test_images1, [
            TextNode("I'm an ", TextType.TEXT),
            TextNode("image", TextType.LINK, "image.jpeg"),
        ])

        image_node2 = TextNode("I'm an ![image](image.jpeg) and I'm a ![second image](image2.jpeg)", TextType.TEXT)

        test_images2 = split_nodes_images([image_node2])

        self.assertEqual(test_images2, [
            TextNode("I'm an ", TextType.TEXT),
            TextNode("image", TextType.LINK, "image.jpeg"),
            TextNode(" and I'm a ", TextType.TEXT),
            TextNode("second image", TextType.LINK, "image2.jpeg")
        ])

    def test_extract_markdown_links(self) -> None:
        test_markdown1 = "I am a [link](google.com)"

        links1 = extract_markdown_links(test_markdown1)
        (text1, url1) = links1[0]

        self.assertEqual(text1, "link")
        self.assertEqual(url1, "google.com")

        test_markdown2 = "I'm a [second](wikipedia.org) [link](google.com)"

        links2 = extract_markdown_links(test_markdown2)
        [( text2_1, url2_1 ), ( text2_2, url2_2 )] = links2

        self.assertEqual(text2_1, "second")
        self.assertEqual(url2_1, "wikipedia.org")
        self.assertEqual(text2_2, "link")
        self.assertEqual(url2_2, "google.com")

        test_markdown3 = ""

        links3 = extract_markdown_links(test_markdown3)

        self.assertEqual(links3, [])

    def test_split_nodes_links(self) -> None:
        link_node1 = TextNode("I'm a [link](google.com) to Google", TextType.TEXT)

        test_links1 = split_nodes_links([link_node1])

        self.assertEqual(test_links1, [
            TextNode("I'm a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "google.com"),
            TextNode(" to Google", TextType.TEXT)
        ])

        link_node2 = TextNode("I'm a [link](google.com) and I'm a [second link](wikipedia.org)", TextType.TEXT)

        test_links2 = split_nodes_links([link_node2])

        self.assertEqual(test_links2, [
            TextNode("I'm a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "google.com"),
            TextNode(" and I'm a ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "wikipedia.org")
        ])

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