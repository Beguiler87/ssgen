import unittest
from main import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType
class TestMarkdownExtraction(unittest.TestCase):
	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
		"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
	def test_extract_markdown_links(self):
		matches = extract_markdown_links(
			"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		)
		self.assertListEqual([
			("to boot dev", "https://www.boot.dev"),
			("to youtube", "https://www.youtube.com/@bootdotdev")
		], matches)
	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode(
					"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
		)
	def test_split_links(self):
		# Test a node with a link at the beginning of the text
		node = TextNode(
			"[Boot.dev](https://boot.dev) is a great place to learn programming",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
				TextNode(" is a great place to learn programming", TextType.TEXT),
			],
			new_nodes,
		)
		# Test a node with no links
		node = TextNode(
			"This text has no links in it",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This text has no links in it", TextType.TEXT),
			],
			new_nodes,
		)
		# Test a node with a link at the end of the text
		node = TextNode(
			"Visit our website at [Boot.dev](https://boot.dev)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("Visit our website at ", TextType.TEXT),
				TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
			],
			new_nodes,
		)
	def test_split_images_additional(self):
		# Test a node with an image at the beginning
		node = TextNode(
			"![Python Logo](https://www.python.org/static/img/python-logo.png) is the Python language logo",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("Python Logo", TextType.IMAGE, "https://www.python.org/static/img/python-logo.png"),
				TextNode(" is the Python language logo", TextType.TEXT),
	 		],
			new_nodes,
		)
		# Test a node with no images
		node = TextNode(
			"This text has no images in it",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This text has no images in it", TextType.TEXT),
			],
			new_nodes,
		)
		# Test multiple images with no text between them
		node = TextNode(
			"Here are two logos: ![Python](https://python.org/logo.png)![Go](https://go.dev/logo.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("Here are two logos: ", TextType.TEXT),
	 			TextNode("Python", TextType.IMAGE, "https://python.org/logo.png"),
				TextNode("Go", TextType.IMAGE, "https://go.dev/logo.png"),
			],
			new_nodes,
		)
		# Test a node with an image at the end
		node = TextNode(
			"The Go mascot is ![Gopher](https://go.dev/blog/gopher/header.jpg)",
			TextType.TEXT,
	 	)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("The Go mascot is ", TextType.TEXT),
				TextNode("Gopher", TextType.IMAGE, "https://go.dev/blog/gopher/header.jpg"),
			],
			new_nodes,
		)
class TestTextToTextNodes(unittest.TestCase):
	def test_simple_text_with_all_formatting(self):
		text = "This is **bold** and _italic_ with `code` and a [link](https://boot.dev)."
		nodes = text_to_textnodes(text)
		expected = [
			TextNode("This is ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode(" and ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" with ", TextType.TEXT),
			TextNode("code", TextType.CODE),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev"),
			TextNode(".", TextType.TEXT),
		]
		self.assertEqual(len(nodes), len(expected))
		for i in range(len(nodes)):
			self.assertEqual(nodes[i].text, expected[i].text)
			self.assertEqual(nodes[i].text_type, expected[i].text_type)
			self.assertEqual(nodes[i].url, expected[i].url)
	def test_nested_formatting(self):
		text = "Here's an ![image](https://example.com/img.png) with **bold _italic_ text**."
		nodes = text_to_textnodes(text)
		expected = [
			TextNode("Here's an ", TextType.TEXT),
			TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
			TextNode(" with ", TextType.TEXT),
			TextNode("bold ", TextType.BOLD),
			TextNode("italic", TextType.ITALIC),
			TextNode(" text", TextType.BOLD),
			TextNode(".", TextType.TEXT),
		]
		self.assertEqual(len(nodes), len(expected))
		for i in range(len(nodes)):
			self.assertEqual(nodes[i].text, expected[i].text)
			self.assertEqual(nodes[i].text_type, expected[i].text_type)
			self.assertEqual(nodes[i].url, expected[i].url)
if __name__ == "__main__":
	unittest.main()
