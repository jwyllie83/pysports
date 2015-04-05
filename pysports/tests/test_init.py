import os
from pysports import parse_text, _parse_all_table_tags, _parse_all_table_names, _parse_all_column_headers
from bs4 import BeautifulSoup

cwd = os.path.dirname(os.path.realpath(__file__))

one_table_full_text = None
one_table_full_text_soup = None

def setup():
	global one_table_full_text
	global one_table_full_text_soup
	with open(cwd + '/drafts_small.html') as handle:
		one_table_full_text = handle.read()
	one_table_full_text_soup = BeautifulSoup(one_table_full_text)

def test_parse_all_table_tags():
	soup = one_table_full_text_soup
	tables = _parse_all_table_tags(soup)
	assert len(tables) == 1
	table = tables[0]
	assert len(table.find_all('tr')) == 7

def test_parse_all_table_names():
	soup = one_table_full_text_soup
	titles = _parse_all_table_names(soup)
	assert len(titles) == 1
	assert type(titles[0]) == unicode
	assert titles[0] == 'Drafted Players'

def test_parse_all_column_headers():
	soup = one_table_full_text_soup
	headers = _parse_all_column_headers(soup)[0]
	assert headers[0].display_name == 'Rk'
	assert headers[0].class_name == 'ranker'
	assert headers[5].display_name == 'Pos'
	assert headers[5].class_name == 'pos'
	assert headers[7].display_name == 'Tm'
	assert len(headers) == 32

def test_parse_text():

	# Test out one table, full text, not many results
	tables = parse_text(one_table_full_text)

	assert len(tables) == 1
	assert 'Search Form' not in [x.title for x in tables]

	test_table = tables[0]
	assert test_table.title == 'Drafted Players'
	assert len(test_table.headers) == 32
#	assert tables[0].valid is True
#	assert len(test_table) == 5
