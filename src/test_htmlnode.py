import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from delimiter import split_nodes_delimiter

class TestHTMLNode(unittest.TestCase):
	def test_props_to_html_with_props(self):
		node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
		self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

	def test_props_to_html_without_props(self):
		node = HTMLNode()
		self.assertEqual(node.props_to_html(), "")

	def test_repr(self):
		node = HTMLNode("p", "Hello", None, {"class": "text"})
		self.assertEqual(repr(node), 'HTMLNode(p, Hello, None, {\'class\': \'text\'})')

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_multiple_attributes(self):
		# creates a LeafNode with multiple attributes for testing
		node = LeafNode(
			"img",
			"Image description",
			{"src": "image.jpg", "alt": "An example image", "class": "thumbnail"}
		)
		# checking exact string comparison is difficult as attributes could be in any order
		html = node.to_html()
		# instead, this checks that all parts are present
		self.assertIn('<img', html)
		self.assertIn('src="image.jpg"', html)
		self.assertIn('alt="An example image"', html)
		self.assertIn('class="thumbnail"', html)
		self.assertIn('>Image description</img>', html)

	def test_leaf_node_no_tag(self):
		# Test a leaf node with no tag (tag=None)
		node = LeafNode(None, "Just some text")
		self.assertEqual(node.to_html(), "Just some text")

	def test_leaf_node_no_value_raises_error(self):
		# Test that a ValueError is raised when value is None
		node = LeafNode("p", None)
		with self.assertRaises(ValueError):
			node.to_html()

	def test_leaf_node_empty_props(self):
		# Test a leaf node with an empty props dictionary
		node = LeafNode("div", "Content", {})
		self.assertEqual(node.to_html(), "<div>Content</div>")

	def test_leaf_node_none_props(self):
		# Test a leaf node with props=None (default)
		node = LeafNode("span", "Some text")  # props defaults to None
		self.assertEqual(node.to_html(), "<span>Some text</span>")

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_split_nodes_delimiter(self):
		# Test 1: Basic case with a single delimiter pair
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		assert len(new_nodes) == 3
		assert new_nodes[0].text == "This is text with a "
		assert new_nodes[0].text_type == TextType.TEXT
		assert new_nodes[1].text == "code block"
		assert new_nodes[1].text_type == TextType.CODE
		assert new_nodes[2].text == " word"
		assert new_nodes[2].text_type == TextType.TEXT

		# Test 2: Multiple delimiter pairs
		node = TextNode("**Bold** and more **bold text**", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		assert len(new_nodes) == 4
		assert new_nodes[0].text == ""  # Empty string before first delimiter
		assert new_nodes[1].text == "Bold"
		assert new_nodes[1].text_type == TextType.BOLD
		assert new_nodes[2].text == " and more "
		assert new_nodes[3].text == "bold text"
		assert new_nodes[3].text_type == TextType.BOLD

		# Test 3: Mixed node types (some should change, some shouldn't)
		node1 = TextNode("Regular text", TextType.TEXT)
		node2 = TextNode("Already bold", TextType.BOLD)
		node3 = TextNode("Text with _italic_ words", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node1, node2, node3], "_", TextType.ITALIC)
		assert len(new_nodes) == 5
		assert new_nodes[1].text_type == TextType.BOLD


if __name__ == "__main__":
	unittest.main()
