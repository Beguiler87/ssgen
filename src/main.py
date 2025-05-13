import re
import os
import shutil
import sys
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from block import BlockType, block_to_block_type
from delimiter import split_nodes_delimiter
def main():
	# get basepath from command line args, default to "/"
	basepath = "/"
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	source = "static"
	destination = "docs"
	if os.path.exists(destination):
		shutil.rmtree(destination)
	os.mkdir(destination)
	recursive_function(source, destination)
	dir_path_content = "content"
	template_path = "template.html"
	dest_dir_path = "docs"
	generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
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
def markdown_to_blocks(markdown):
	# split the markdown by double newlines
	blocks = markdown.split("\n\n")
	# clean up the blocks
	cleaned_blocks = []
	for block in blocks:
		# strip leading/trailing whitespace
		cleaned_block = block.strip()
		# only add non-empty blocks
		if cleaned_block:
			cleaned_blocks.append(cleaned_block)
	return cleaned_blocks
def text_to_children(text):
	text = ' '.join(text.split())
	# parse text into TextNode objects
	text_nodes = text_to_textnodes(text)
	# convert each TextNode to an HTMLNode
	html_nodes = []
	for text_node in text_nodes:
		html_node = text_node_to_html_node(text_node)
		html_nodes.append(html_node)
	return html_nodes
def count_heading_level(block):
	# counts number of # at the beginning of the block
	level = 0
	for char in block:
		if char == '#':
			level += 1
		else:
			break
	return min(level, 6)
def extract_code_block_content(block):
	# remove open/closing triple backticks and any language identifier
	lines = block.split("\n")
	# skip first and last lines (which contain the backticks)
	content_lines = lines[1:-1] if len(lines) > 2 else []
	return "\n".join(content_lines)
def markdown_to_html_node(markdown):
	converted_blocks = markdown_to_blocks(markdown)
	nodes = []
	for block in converted_blocks:
		block_type = block_to_block_type(block)
		if block_type == BlockType.PARAGRAPH:
			node = HTMLNode(
				tag="p",
				value=None,
				children=text_to_children(block),
			)
			nodes.append(node)
		elif block_type == BlockType.HEADING:
			# Get the heading level (h1, h2, etc.) - you'll need a helper function
			level = count_heading_level(block)  # This would count the number of # symbols
			node = HTMLNode(
				tag=f"h{level}",
				value=None,
				children=text_to_children(block.lstrip("#").strip()),  # Remove the # symbols
			)
			nodes.append(node)
		elif block_type == BlockType.CODE:
			lines = block.strip().split('\n')
			# Skip the first and last lines (which contain ```)
			# and extract just the content
			content_lines = []
			parsing = False
			for line in lines:
				if line.strip() == '```' and not parsing:
					parsing = True
					continue
				elif line.strip() == '```' and parsing:
					break
				elif parsing:
					# strip any leading/trailing whitespace and tabs
					content_lines.append(line.strip())
			# Join the content lines and add the final newline
			code_content = '\n'.join(content_lines) + '\n'
			# for testing
			# print(f"Code block content: {repr(code_content)}")
			# Create the nodes
			text_node = TextNode(code_content, TextType.TEXT)
			code_node = HTMLNode(tag="code", children=[text_node_to_html_node(text_node)])
			pre_node = HTMLNode(tag="pre", children=[code_node])
			nodes.append(pre_node)
		elif block_type == BlockType.QUOTE:
			quote_content = []
			for line in block.split('\n'):
				if line.startswith('> '):
					line = line[2:]
				elif line.startswith('>'):
					line = line[1:]
				quote_content.append(line)
			quote_text = '\n'.join(quote_content)
			node = HTMLNode(
				tag="blockquote",
				value=None,
				children=text_to_children(quote_text),
			)
			nodes.append(node)
		elif block_type == BlockType.UNORDERED_LIST:
			# Create the container ul node
			ul_node = HTMLNode(tag="ul", value=None, children=[])
			# Process each list item
			for line in block.split('\n'):
				# Skip empty lines
				if not line.strip():
					continue
				# Remove the list marker (-, *, or +) and the space after it
				if line.strip().startswith(('-', '*', '+')):
					# Find the position after the marker and the following space
					content_start = line.find(line.strip()[0]) + 2
					item_content = line[content_start:]
					# Create the li node for this item
					li_node = HTMLNode(
						tag="li",
						value=None,
						children=text_to_children(item_content),
					)
					ul_node.children.append(li_node)
			nodes.append(ul_node)
		elif block_type == BlockType.ORDERED_LIST:
			# Create the container ol node
			ol_node = HTMLNode(tag="ol", value=None, children=[])
			
			# Process each list item
			for line in block.split('\n'):
				# Skip empty lines
				if not line.strip():
					continue
				# Check for numbered list pattern (like "1. " or "42. ")
				stripped_line = line.strip()
				if stripped_line and stripped_line[0].isdigit():
					# Find the position of the period and the space after it
					for i, char in enumerate(stripped_line):
						if char == '.' and i+1 < len(stripped_line) and stripped_line[i+1] == ' ':
							# Extract the content after the number, period, and space
							item_content = stripped_line[i+2:]
							
							# Create the li node for this item
							li_node = HTMLNode(
								tag="li",
								value=None,
								children=text_to_children(item_content),
							)
							ol_node.children.append(li_node)
							break
			nodes.append(ol_node)
	# Create a parent div node and add all blocks as children
	parent_node = HTMLNode(
		tag="div",
		value=None,
		children=nodes,
	)
	return parent_node
def extract_title(markdown):
	# looks for a line that starts with a single "#"
	for line in markdown.split("\n"):
		line = line.strip()
		if line.startswith("#") and not line.startswith("##"):
			# make sure there's a space after the #
			if len(line) > 1 and line[1] == " ":
				return line[2:].strip()
	# if we didn't find an h1 header, raise an exception
	raise Exception("No h1 header found in markdown")
def generate_page(from_path, template_path, dest_path, basepath="/"):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	# Check if input files exist
	print(f"Does {from_path} exist? {os.path.exists(from_path)}")
	print(f"Does {template_path} exist? {os.path.exists(template_path)}")
	# read the markdown file
	with open(from_path, 'r') as f:
		markdown_content = f.read()
	# read the template file
	with open(template_path, 'r') as f:
		template_content = f.read()
	# convert markdown to HTML with existing functions
	html_node = markdown_to_html_node(markdown_content)
	html_content = html_node.to_html()
	# estract the title
	title = extract_title(markdown_content)
	# replace placeholders
	final_html = template_content.replace("{{ Title }}", title)
	final_html = final_html.replace("{{ Content }}", html_content)
	# ensure directory exists
	os.makedirs(os.path.dirname(dest_path), exist_ok=True)
	# write the output file
	with open(dest_path, 'w') as f:
		f.write(final_html)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
	# Walk through the content directory recursively
	for root, dirs, files in os.walk(dir_path_content):
		for file in files:
			if file.endswith(".md"):
				# Get the full path of the markdown file
				markdown_path = os.path.join(root, file)
				# Calculate the destination path in the public directory
				# Replace content dir with destination dir and ".md" with ".html"
				rel_path = os.path.relpath(markdown_path, dir_path_content)
				destination_path = os.path.join(dest_dir_path, os.path.splitext(rel_path)[0] + ".html")
				# Ensure the parent directory exists
				os.makedirs(os.path.dirname(destination_path), exist_ok=True)
				# Generate the page
				generate_page(markdown_path, template_path, destination_path)
def recursive_function(src, dst):
	directory_list = os.listdir(src)
	for directory_item in directory_list:
		source_path = os.path.join(src, directory_item)
		destination_path = os.path.join(dst, directory_item)
		if os.path.isfile(source_path):
			shutil.copy(source_path, destination_path)
			print(destination_path)
		elif os.path.isdir(source_path):
			if not os.path.exists(destination_path):
				os.mkdir(destination_path)
			recursive_function(source_path, destination_path)
# calls main function when script is run
if __name__ == "__main__":
	main()
