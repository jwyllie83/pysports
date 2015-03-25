__doc__ = """
Parses sports-reference.com defined data tables into internal data structures
for easier processing.  

Parsing functions:

- parse_handle() -- Takes an open file handle and reads stats tables out of it
- parse_text() -- Takes a blob of text and reads stats tables out of it
- parse_URI() -- Takes a URI, loads it, and reads stats tables out of it

See ../README.md for more details.
"""

### By the way, don't use this as some kind of example of how to parse with
### BeautifulSoup or anything.  I'm skimming the guide at
### http://www.crummy.com/software/BeautifulSoup/bs4/doc/ to do all of this and
### translating into BSv3 as I go.  It's not like I'm a pro at HTML parsing or
### anything, and I'm sure there are far better ways to do what I'm looking to
### do here

import sys
from pysports import *
from pysports import structures
from BeautifulSoup import BeautifulSoup
import logging

def parse_text(stats_dump):
	"""Reads stats out of a blob of text"""
	log = logging.getLogger('pysports.parse_text')
	soup = BeautifulSoup(stats_dump)
	log.debug('Successfully parsed the stats text with BeautifulSoup')

	# Find the tables as Soup tag trees
	table_tags = _parse_all_table_tags(soup)
	log.debug('Found %d data tables' % len(table_tags))
	tables = []

	for tag in table_tags:
		tables.append(structures.Table())

	# Give the tables some titles
	table_titles = _parse_all_table_names(soup)
	log.debug('Found %d data table titles on parsing' % len(table_titles))
	if len(table_titles) != len(tables):
		log.error('Data tables != data table titles count.  Parsing failed; bailing out')
		raise ValueError('Number of parsed titles (%d) != number of parsed statistics tables (%d)' % (len(table_titles), len(tables)))

	for index, table_title in enumerate(table_titles):
		tables[index].title = table_title

	# Figure out the column headers for the table

	return tables


def _parse_all_table_tags(soup):
	"""Internal function to grab all <table> BeautifulSoup tags corresponding to data tables in the HTML"""

	tables = []
	# Parse out statistics tables based on class identifiers
	for potential_table in soup.findAll('table'):
		if potential_table.get('class') is not None and \
				'stats_table' in potential_table.get('class') and \
				'form_table' not in potential_table.get('class'):
			tables.append(potential_table)

	return tables

def _parse_all_table_names(soup):
	"""Internal function to figure out all of the table headings corresponding to data tables in the HTML"""

	# Figure out all the table names
	# This is complicated because it turns out the identifiers for these headings aren't that straightforward...
	headings = []
	for potential_heading in soup.findAll('div'):

		# If it looks like it's the heading div for a table...
		if potential_heading.get('class') is not None and potential_heading.get('class') == 'table_heading':

			# If it happens to have a large heading:
			if potential_heading.h2 is not None:

				search_text = potential_heading.h2.contents[0]

			if search_text != 'Search Form':
				headings.append(potential_heading.h2.a.contents[0])

	return headings
