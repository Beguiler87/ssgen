from enum import Enum
class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"
def block_to_block_type(block):
	# most logical order: code, headings, quotes, unordered lists, ordered lists, paragraphs
	lines = block.split("\n")
	# CODE
	if len(lines) >= 2:
		first_line = lines[0].strip()
		last_line = lines[-1].strip()
		if first_line.startswith("```") and last_line == "```":
			return BlockType.CODE
	# HEADINGS
	if block.startswith("#"):
		# split first line to separate the symbols from the text
		first_line = block.split("\n")[0]
		# count the consecutive # symbols at the beginning
		heading_level = 0
		for char in first_line:
			if char == '#':
				heading_level += 1
			else:
				break
		# valid heading: 1-6 # symbols followed by a space
		if 1 <= heading_level <= 6 and first_line[heading_level:heading_level+1] == " ":
			return BlockType.HEADING
	# QUOTES
	# checks if it's a quote block
	is_quote = True
	for line in lines:
		if not line.startswith(">"):
			is_quote = False
			break
	if is_quote and lines:
		return BlockType.QUOTE
	# UNORDERED_LIST
	is_unordered_list = True
	for line in lines:
		if not line.startswith("- "):
			is_unordered_list = False
			break
	if is_unordered_list and lines:
		return BlockType.UNORDERED_LIST
	# ORDERED_LIST
	if lines:
		is_ordered_list = True
		expected_number = 1
		for line in lines:
			expected_prefix = f"{expected_number}. "
			if not line.startswith(expected_prefix):
				is_ordered_list = False
				break
			expected_number += 1
		if is_ordered_list:
			return BlockType.ORDERED_LIST
	# PARAGRAPH
	return BlockType.PARAGRAPH
