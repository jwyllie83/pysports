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
from bs4 import BeautifulSoup
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
	log.debug('Looking for column headers...')
	column_headers = _parse_all_column_headers(soup)
	log.debug('Found %d sets of column headers' % len(column_headers))
	for index, column_header_set in enumerate(column_headers):
		tables[index].headers = column_header_set

	return tables


def _parse_all_table_tags(soup):
	"""Internal function to grab all <table> BeautifulSoup tags corresponding to data tables in the HTML"""

	tables = []
	# Parse out statistics tables based on class identifiers
	for potential_table in soup.find_all('table'):
		if potential_table.get('class') is not None and \
				'stats_table' in potential_table.get('class') and \
				'form_table' not in potential_table.get('class'):
			tables.append(potential_table)

	return tables

def _parse_all_table_names(soup):
	"""Internal function to figure out all of the table headings corresponding to data tables in the HTML"""

	log = logging.getLogger('pysports._parse_all_table_names')

	# Figure out all the table names
	# This is complicated because it turns out the identifiers for these headings aren't that straightforward...
	headings = []
	for potential_heading in soup.find_all('div'):

		if potential_heading.has_attr('class') is False:
			continue

		# Looks like a table header...
		if 'table_heading' in potential_heading['class']:

			# ... make sure it's not the search box
			if u'Search Form' in [unicode(x) for x in potential_heading.stripped_strings]:
				continue

			# If it happens to have a large heading:
			search_text = None
			if potential_heading.h2 is not None:
				search_text = unicode(potential_heading.h2.string)
			headings.append(search_text)

	return headings

def _parse_all_column_headers(soup):
	"""Find all of the column headers and parse them"""

	log = logging.getLogger('pysports._parse_all_column_headers')
	return_column_headers = []

	# First, grab all of the potential table soup bowls...
	tables = _parse_all_table_tags(soup)

	for table in tables:

		all_column_headers = []

		# Get all of the header rows
		potential_tr = table.thead
		potential_trs = table.find_all('tr')
		for potential_tr in potential_trs:

			# There can be a "top header" on a document. Throw that out.
			if 'over_header' in potential_tr.get('class'):
				continue

			stat_finder = {'data-stat' : True}
			all_ths = potential_tr.find_all('th', attrs=stat_finder)
			for stat_th in all_ths:

				# Got a new column header: build it and add it to the list
				new_header = structures.ColumnHeader()
				new_header.display_name = unicode(stat_th.get_text())
				new_header.class_name = unicode(stat_th['data-stat'])

				log.debug(str(new_header))
				all_column_headers.append(new_header)

		return_column_headers.append(all_column_headers)

	return return_column_headers
