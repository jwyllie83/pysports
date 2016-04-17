__doc__ = """
Parses sports-reference.com defined data tables into internal data structures
for easier processing.  

Parsing functions:

- parse_text() -- Takes a blob of text and reads stats tables out of it

See ../README.md for more details.
"""

### By the way, don't use this as some kind of example of how to parse with
### BeautifulSoup or anything.  I'm skimming the guide at
### http://www.crummy.com/software/BeautifulSoup/bs4/doc/ to do all of this.
### It's not like I'm a pro at HTML parsing or anything, and I'm sure there are
### far better ways to do what I'm looking to do here
###
### (Author's note: there's a better way to do this, at least: after writing,
### I figured out that you can pass around decomposed BeautifulSoup objects
### rather than re-parsing the whole structure.  It's a far, far better and
### cleaner way to do this.  I'm not going to re-write it, but, if you're
### wondering why that's done... that's why)

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

	# Go get all of the row sets for the tables
	log.debug('Looking for rows...')
	row_sets, total_rows = _parse_all_data(soup)
	log.debug('Found %d sets of rows' % len(row_sets))
	for index, rows in enumerate(row_sets):
		for row in rows:
			tables[index].append(row)
			tables[index].total_row = total_rows[index]

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

			# There's this annoying thing in new formats where they report draft pick trades on some draft
			# pages.  I'm really not sure what to do about it programmatically: you'd need to know adjacent
			# tags to know that there's no table after it.  For now, I'll filter it out, but it's brittle.
			if u'Draft Pick Trades' in [unicode(x) for x in potential_heading.stripped_strings]:
				continue

			# If it happens to have a large heading:
			search_text = None
			if potential_heading.h2 is not None:
				search_text = unicode(potential_heading.h2.string)
			if potential_heading.h3 is not None:
				search_text = unicode(potential_heading.h3.string)
			headings.append(search_text)

	return headings

def _parse_all_column_headers(soup):
	"""Find all of the column headers and parse them.  Will only parse the first of (potentially many) header rows."""

	log = logging.getLogger('pysports._parse_all_column_headers')
	return_column_headers = []

	# Some tables have repeat header rows.  Only save the first one.
	found_headers = False

	# First, grab all of the potential table soup bowls...
	tables = _parse_all_table_tags(soup)

	for table in tables:

		all_column_headers = []
		found_headers = False

		# Get all of the header rows
		potential_tr = table.thead
		potential_trs = table.find_all('tr')
		for potential_tr in potential_trs:

			# Found a header row and fully parsed it already?  Let's get out of here.
			if found_headers == True:
				break

			# There can be a "top header" on a document. Throw that out.
			if potential_tr.has_attr('class') is True and 'over_header' in potential_tr.get('class'):
				continue

			# There are some tables that are completely bare-bones.  No over-header present.  It looks, however,
			# like the over-headers are reliably labeled.  If that's the case, just throw those out and grab 
			# everything else.  Hopefully this works reliably enough.
			all_ths = potential_tr.find_all('th')
			for stat_th in all_ths:

				# Got a new column header: build it and add it to the list
				new_header = structures.ColumnHeader()
				new_header.display_name = unicode(stat_th.get_text())
				if new_header.display_name == '':
					new_header.display_name = None
				if stat_th.has_attr('data-stat') is True:
					new_header.class_name = stat_th['data-stat'].encode('utf-8')

				log.debug(str(new_header))
				all_column_headers.append(new_header)
				found_headers = True

		return_column_headers.append(all_column_headers)

	return return_column_headers

def _parse_all_data(soup):
	"""Find all of the data points in each of the tables and add them in"""

	log = logging.getLogger('pysports._parse_all_data')
	return_rows = []
	return_total = []

	# Again, get all of the tables...
	tables = _parse_all_table_tags(soup)

	# ... get all of the rows, in order
	for table in tables:

		new_rows = []
		new_total = None

		all_potential_rows = table.find_all('tr')
		for potential_row in all_potential_rows:

			total_row = False

			# There's no good way to identify a row, so we have to identify it by the non-presence of headers
			if potential_row.th is not None:
				continue

			new_row = structures.Row()
			row = potential_row
			cells = row.find_all('td')

			# Some tables are compressed, with a single row having "Show All..." in it.  We don't save that.
			if len(cells) == 1 and 'Show All' in cells[0].get_text():
				continue

			for cell in cells:
				# Colspans are one way to identify a "total row" with summary info, though not the only one.
				if cell.has_attr('colspan') is True:
					total_row = True
				new_row.sieve(cell.get_text())

			# Some tables have a "Totals" row at the bottom.  You can easily calculate that from the data.  If
			# this gets put in, just stick it in as an appendix to the table, not with the data.
			if (row.has_attr('class') and 'stat_total' in row['class']) or total_row is True:
				new_total = new_row
			else:
				new_rows.append(new_row)

		return_rows.append(new_rows)
		return_total.append(new_total)

	return (return_rows, return_total)
