import unittest
from block import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
	def test_paragraphs(self):
		# Simple paragraph
		self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
		# Multi-line paragraph
		self.assertEqual(block_to_block_type("This is a\nmulti-line paragraph."), BlockType.PARAGRAPH)
		# Paragraph with special characters (but not at the start of lines)
		self.assertEqual(block_to_block_type("This has # but not at start\nAnd > here too"), BlockType.PARAGRAPH)
		# Empty block
		self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
	def test_headings(self):
		# H1 heading
		self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
		# H6 heading (max level)
		self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
		# Heading with multiple lines
		self.assertEqual(block_to_block_type("# Heading\nwith second line"), BlockType.HEADING)
		# Invalid heading (no space after #)
		self.assertEqual(block_to_block_type("#Invalid heading"), BlockType.PARAGRAPH)
		# Invalid heading (too many #)
		self.assertEqual(block_to_block_type("####### Too many hashtags"), BlockType.PARAGRAPH)
	def test_code_blocks(self):
		# Simple code block
		self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
		# Empty code block
		self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)
		# Multi-line code block
		self.assertEqual(block_to_block_type("```\nline 1\nline 2\nline 3\n```"), BlockType.CODE)
		# Code block with language specified
		self.assertEqual(block_to_block_type("```python\ndef hello():\n    print('Hello')\n```"), BlockType.CODE)
		# Invalid code block (missing closing backticks)
		self.assertEqual(block_to_block_type("```\ncode here"), BlockType.PARAGRAPH)
		# Invalid code block (missing opening backticks)
		self.assertEqual(block_to_block_type("code here\n```"), BlockType.PARAGRAPH)
	def test_quote_blocks(self):
		# Simple quote
		self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
		# Multi-line quote
		self.assertEqual(block_to_block_type(">Line 1\n>Line 2\n>Line 3"), BlockType.QUOTE)
		# Quote with empty lines (still prefixed with >)
		self.assertEqual(block_to_block_type(">Line 1\n>\n>Line 3"), BlockType.QUOTE)
		# Invalid quote (missing > on one line)
		self.assertEqual(block_to_block_type(">Line 1\nLine 2\n>Line 3"), BlockType.PARAGRAPH)
	def test_unordered_lists(self):
		# Simple unordered list
		self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
		# Multi-item unordered list
		self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
		# Invalid unordered list (missing space after -)
		self.assertEqual(block_to_block_type("-Item 1\n-Item 2"), BlockType.PARAGRAPH)
		# Invalid unordered list (one line without -)
		self.assertEqual(block_to_block_type("- Item 1\nItem 2\n- Item 3"), BlockType.PARAGRAPH)
	def test_ordered_lists(self):
		# Simple ordered list
		self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
		# Multi-item ordered list
		self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)
		# Invalid ordered list (wrong numbering)
		self.assertEqual(block_to_block_type("1. Item 1\n3. Item 2"), BlockType.PARAGRAPH)
		# Invalid ordered list (not starting at 1)
		self.assertEqual(block_to_block_type("2. Item 1\n3. Item 2"), BlockType.PARAGRAPH)
		# Invalid ordered list (missing space after dot)
		self.assertEqual(block_to_block_type("1.Item 1\n2.Item 2"), BlockType.PARAGRAPH)
		# Invalid ordered list (non-sequential)
		self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n4. Item 3"), BlockType.PARAGRAPH)
if __name__ == "__main__":
	unittest.main()