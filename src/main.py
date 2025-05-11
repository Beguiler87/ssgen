import re
from textnode import TextNode, TextType
def main():
	# dummy node for texting purposes.
	node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
	print(node)
def extract_markdown_images(text):
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches
def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches
def extract_markdown_bold(text):
	matches = re.findall(r"\*\*([^\*\*]*)\*\*", text)
	return matches
def extract_markdown_italic(text):
	matches = re.findall(r"_([^_]*)_", text)
	return matches
def extract_markdown_code(text):
	matches = re.findall(r"`([^`]*)`", text)
	return matches
def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		images = extract_markdown_images(old_node.text)
		if not images:
			new_nodes.append(old_node)
			continue
		remaining_text = old_node.text
		for image in images:
			# splits the text at image markdown
			image_markdown = f"![{image[0]}]({image[1]})"
			parts = remaining_text.split(image_markdown, 1)
			# add text before the image if not empty
			if parts[0]:
				new_nodes.append(TextNode(parts[0], TextType.TEXT))
			# add the image node
			new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
			# update remaining text
			if len(parts) > 1:
				remaining_text = parts[1]
			else:
				remaining_text = ""
		# add any reaining text after the last image
		if remaining_text:
			new_nodes.append(TextNode(remaining_text, TextType.TEXT))
	return new_nodes
def split_nodes_link(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		links = extract_markdown_links(old_node.text)
		if not links:
			new_nodes.append(old_node)
			continue
		remaining_text = old_node.text
		for link in links:
			# splits the text at link markdown
			link_markdown = f"[{link[0]}]({link[1]})"
			parts = remaining_text.split(link_markdown, 1)
			# add text before the link if not empty
			if parts[0]:
				new_nodes.append(TextNode(parts[0], TextType.TEXT))
			# add the link node
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			# update remaining text
			if len(parts) > 1:
				remaining_text = parts[1]
			else:
				remaining_text = ""
		# add any remaining text after the last link
		if remaining_text:
			new_nodes.append(TextNode(remaining_text, TextType.TEXT))
	return new_nodes
def split_nodes_bold(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		# Skip special nodes
		if old_node.text_type in [TextType.IMAGE, TextType.LINK]:
			new_nodes.append(old_node)
			continue
		# Extract bold sections
		bold_sections = extract_markdown_bold(old_node.text)
		# If no bold sections found, keep the node as is
		if not bold_sections:
			new_nodes.append(old_node)
			continue
		# Process the text, splitting at each bold section
		remaining_text = old_node.text
		for bold_text in bold_sections:
			# Create the markdown pattern to split on
			bold_markdown = f"**{bold_text}**"
			# Split the text at the markdown
			parts = remaining_text.split(bold_markdown, 1)
			# Add text before the bold section if it exists
			if parts[0]:
				new_nodes.append(TextNode(parts[0], old_node.text_type))
			# Add the bold section
			new_nodes.append(TextNode(bold_text, TextType.BOLD))
			# Update remaining text
			if len(parts) > 1:
				remaining_text = parts[1]
			else:
				remaining_text = ""
		# Add any remaining text after the last bold section
		if remaining_text:
			new_nodes.append(TextNode(remaining_text, old_node.text_type))
	return new_nodes
def split_nodes_italic(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		# skip special nodes with urls like images and links
		if old_node.text_type in [TextType.IMAGE, TextType.LINK]:
			new_nodes.append(old_node)
			continue
		# Extract italic sections
		italic_sections = extract_markdown_italic(old_node.text)
		# If no italic sections found, keep the node as is
		if not italic_sections:
			new_nodes.append(old_node)
			continue
		# Process the text, splitting at each italic section
		remaining_text = old_node.text
		for italic_text in italic_sections:
			# Create the markdown pattern to split on
			italic_markdown = f"_{italic_text}_"
			# Split the text at the markdown
			parts = remaining_text.split(italic_markdown, 1)
			# Add text before the italic section if it exists
			if parts[0]:
				new_nodes.append(TextNode(parts[0], old_node.text_type))
			# Add the italic section
			new_nodes.append(TextNode(italic_text, TextType.ITALIC))
			# Update remaining text
			if len(parts) > 1:
				remaining_text = parts[1]
			else:
				remaining_text = ""
		# Add any remaining text after the last italic section
		if remaining_text:
			new_nodes.append(TextNode(remaining_text, old_node.text_type))
	return new_nodes
def split_nodes_code(old_nodes):
		new_nodes = []
		for old_node in old_nodes:
				# skip special nodes
				if old_node.text_type in [TextType.IMAGE, TextType.LINK]:
						new_nodes.append(old_node)
						continue
				# Extract code sections
				code_sections = extract_markdown_code(old_node.text)
				# If no code sections found, keep the node as is
				if not code_sections:
						new_nodes.append(old_node)
						continue
				# Process the text, splitting at each code section
				remaining_text = old_node.text
				for code_text in code_sections:
						# Create the markdown pattern to split on
						code_markdown = f"`{code_text}`"
						# Split the text at the markdown
						parts = remaining_text.split(code_markdown, 1)
						# Add text before the code section if it exists
						if parts[0]:
								new_nodes.append(TextNode(parts[0], TextType.TEXT))
						# Add the code section
						new_nodes.append(TextNode(code_text, TextType.CODE))
						# Update remaining text
						if len(parts) > 1:
								remaining_text = parts[1]
						else:
								remaining_text = ""
				# Add any remaining text after the last code section
				if remaining_text:
						new_nodes.append(TextNode(remaining_text, TextType.TEXT))
		return new_nodes
def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_code(nodes)
	nodes = split_nodes_bold(nodes)
	nodes = split_nodes_italic(nodes)
	return nodes
# calls main function when script is run
if __name__ == "__main__":
	main()
