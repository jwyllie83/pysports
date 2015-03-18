__doc__ = """
Parses sports-reference.com defined data tables into internal data structures
for easier processing.  

Parsing functions:

- parse_handle() -- Takes an open file handle and reads stats tables out of it
- parse_text() -- Takes a blob of text and reads stats tables out of it
- parse_URI() -- Takes a URI, loads it, and reads stats tables out of it

See ../README.md for more details.
"""

import sys
from pysports import *
from BeautifulSoup import BeautifulSoup

def parse_text(stats_dump):
	"""Reads stats out of a blob of text"""
	soup = BeautifulSoup(stats_dump)
	tables = []

	# Parse out statistics tables based on class identifiers
	for potential_table in soup.findAll('table'):
		if potential_table.get('class') is not None and \
				'stats_table' in potential_table.get('class') and \
				'form_table' not in potential_table.get('class'):
			tables.append(potential_table)

	pass
	assert False
