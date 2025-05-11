from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		# compares 'other' to make sure it's also a TextNode object
		if not isinstance(other, TextNode):
			return False
		# then compares all other properties one by one
		return (self.text == other.text and
			self.text_type == other.text_type and
			self.url == other.url)

	def __repr__(self):
		# returns a string representation of the TextNode
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
	# return a leafnode with no tag, just the text value
	if text_node.text_type == TextType.TEXT:
		return LeafNode(None, text_node.text)
	# return a leafnode with a "b" tag and the text
	elif text_node.text_type == TextType.BOLD:
		return LeafNode("b", text_node.text)
	# return a leafnode with an "i" tag and the text
	elif text_node.text_type == TextType.ITALIC:
		return LeafNode("i", text_node.text)
	# handle other types
	elif text_node.text_type == TextType.CODE:
		return LeafNode("code", text_node.text)
	elif text_node.text_type == TextType.LINK:
		props = {"href": text_node.url}
		return LeafNode("a", text_node.text, props)
	elif text_node.text_type == Text_Type.IMAGE:
		props = {
			"src": text_node.url,
			"alt": text_node.text
		}
		return LeafNode("img", "", props)
	# raise an exception for unhandled texttype
	else:
		raise Exception(f"Invalid text type: {text_node.text_type}")
