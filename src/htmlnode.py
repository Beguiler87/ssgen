class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
	def to_html(self):
		# If this is a text node (no tag), just return the value
		if self.tag is None:
			return self.value or ""
		# Start building the HTML with the opening tag
		html = f"<{self.tag}"
		# Add any attributes
		if self.props:
			for attr, value in self.props.items():
				html += f' {attr}="{value}"'
		# Close the opening tag
		html += ">"
		# Add the value/text content if any
		if self.value:
			html += self.value
		# Add all children's HTML
		if self.children:
			for child in self.children:
				html += child.to_html()
		# Add the closing tag
		html += f"</{self.tag}>"
		return html
	def props_to_html(self):
		# if the value of props is None we return an empty string
		if self.props is None:
			return ""
		# creates an empty string to store the incoming HTML attributes
		result = ""
		# gets key-value pairs from the dictionary, formats it in key="value", and adds it to the result
		for key, value in self.props.items():
			result += f' {key}="{value}"'
		return result
	def __repr__(self):
		# creates a string that shows tag, value, children, and props of the node.
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, [], props)
	# method to render leaf node as HTML string
	def to_html(self):
		if self.value == None:
			raise ValueError("LeafNode must have a value")
		elif self.tag == None:
			return self.value
		else:
			if self.props and len(self.props) > 0:
				props_str = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
				return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
			else:
				return f"<{self.tag}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props=None)
	# method to render parent node
	def to_html(self):
		if self.tag == None:
			raise ValueError("ParentNode must have a tag")
		elif self.children == None:
			raise ValueError("ParentNode must have children")
		elif  len(self.children) ==0:
			raise ValueError("ParentNode must have children")
		else:
			children_html = ""
			for child in self.children:
				children_html += child.to_html()
			return f"<{self.tag}>{children_html}</{self.tag}>"
