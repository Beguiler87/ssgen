from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	result = []
	for old_node in old_nodes:
		# checks to make sure the input is of the correct type. If it isn't, it gets added to the result with no changes.
		if old_node.text_type != TextType.TEXT:
			result.append(old_node)
			continue
		# find and process delimiter pairs in the text
		# split the text by delimiter
		parts = old_node.text.split(delimiter)
		# if there is an odd number of parts, the delimiters aren't balanced, so raise an exception
		if len(parts) % 2 == 0:
			raise ValueError(f"Unbalanced delimiters in text: {old_node.text}")
		# process parts
		for i in range(len(parts) - 1): # skip the last part if it's empty
			# even index parts are outside the delimiter (including first and last)
			if i % 2 == 0:
				result.append(TextNode(parts[i], TextType.TEXT))
			else: # odd index parts are inside the delimiter
				result.append(TextNode(parts[i], text_type))
		# only add the last part if it's not empty
		if parts[-1]:
			result.append(TextNode(parts[-1], TextType.TEXT))
	return result
