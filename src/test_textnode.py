import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	# checks if two identical TextNode objects are equal
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	# checks if two TextNode objects with different text are not equal
	def test_different_text(self):
		node1 = TextNode("Text one", TextType.BOLD)
		node2 = TextNode("Text two", TextType.BOLD)
		self.assertNotEqual(node1, node2)

	# tests when the URL property is None
	def test_url_property(self):
		# two nodes with None urls shoudl be equal if other properties match
		node1 = TextNode("Some text", TextType.BOLD)
		node2 = TextNode("Some text", TextType.BOLD)
		self.assertEqual(node1, node2)

		# a node with a url should not equal a node without a url
		node3 = TextNode("Some text", TextType.BOLD, "https://example.com")
		self.assertNotEqual(node1, node3)

	# tests for differing text types
	def test_text_type_property(self):
		# nodes with different text types should not be equal
		node1 = TextNode("Same text", TextType.BOLD)
		node2 = TextNode("Same text", TextType.ITALIC)
		self.assertNotEqual(node1, node2)

		# nodes with same text type should be equal if other properties match
		node3 = TextNode("Same text", TextType.CODE)
		node4 = TextNode("Same text", TextType.CODE)
		self.assertEqual(node3, node4)

		# even with urls, test type differences should make nodes not equal
		node5 = TextNode("Same text", TextType.BOLD, "https://example.com")
		node6 = TextNode("Same text", TextType.ITALIC, "https://example.com")
		self.assertNotEqual(node5, node6)

if __name__ == "__main__":
	unittest.main()
