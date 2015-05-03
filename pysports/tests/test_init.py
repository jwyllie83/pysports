import os
from pysports import parse_text, _parse_all_table_tags, _parse_all_table_names, _parse_all_column_headers, _parse_all_data
from bs4 import BeautifulSoup

cwd = os.path.dirname(os.path.realpath(__file__))

one_table_full_text = None
one_table_full_text_soup = None

complicated = None
complicated_soup = None

multiple_headers = None
multiple_headers_soup = None

def setup():
	global one_table_full_text
	global one_table_full_text_soup

	global complicated
	global complicated_soup

	global multiple_headers
	global multiple_headers_soup

	with open(cwd + '/drafts_small.html') as handle:
		one_table_full_text = handle.read()
	one_table_full_text_soup = BeautifulSoup(one_table_full_text)

	with open(cwd + '/superbowl_complicated.html') as handle:
		complicated = handle.read()
	complicated_soup = BeautifulSoup(complicated)

	with open(cwd + '/single_table_multiple_headers.html') as handle:
		multiple_headers = handle.read()
	multiple_headers_soup = BeautifulSoup(multiple_headers)

def test_parse_all_table_tags():
	soup = one_table_full_text_soup
	tables = _parse_all_table_tags(soup)
	assert len(tables) == 1
	table = tables[0]
	assert len(table.find_all('tr')) == 7

	soup = complicated_soup
	tables = _parse_all_table_tags(soup)
	assert len(tables) == 9
	assert len(tables[0].find_all('tr')) == 4
	assert len(tables[1].find_all('tr')) == 6
	assert len(tables[5].find_all('tr')) == 16

	soup = multiple_headers_soup
	tables = _parse_all_table_tags(soup)
	assert len(tables) == 1

def test_parse_all_table_names():
	soup = one_table_full_text_soup
	titles = _parse_all_table_names(soup)
	assert len(titles) == 1
	assert type(titles[0]) == unicode
	assert titles[0] == 'Drafted Players'

	soup = complicated_soup
	titles = _parse_all_table_names(soup)
	assert len(titles) == 9
	assert titles[1] == 'To Go'
	assert titles[3] == 'Team Defense'
	assert titles[8] == 'Individual Plays'

	soup = multiple_headers_soup
	titles = _parse_all_table_names(soup)
	assert len(titles) == 1
	assert titles[0] == 'Drafted Players'


def test_parse_all_column_headers():
	soup = one_table_full_text_soup
	all_headers = _parse_all_column_headers(soup)
	headers = all_headers[0]
	assert headers[0].display_name == 'Rk'
	assert headers[0].class_name == 'ranker'
	assert headers[5].display_name == 'Pos'
	assert headers[5].class_name == 'pos'
	assert headers[7].display_name == 'Tm'
	assert len(headers) == 32

	soup = complicated_soup
	all_headers = _parse_all_column_headers(soup)
	assert len(all_headers) == 9
	assert len(all_headers[0]) == 3
	assert all_headers[0][0].display_name == 'Down'
	assert all_headers[0][0].class_name is None
	assert len(all_headers[2]) == 15
	assert all_headers[2][0].display_name == 'Tm'
	assert all_headers[2][0].class_name is None
	assert all_headers[2][5].display_name == '1st%'
	assert all_headers[2][5].class_name is None
	assert len(all_headers[3]) == 15
	assert len(all_headers[8]) == 14
	assert all_headers[8][13].display_name is None
	assert all_headers[8][13].class_name == 'exp_pts_diff'

	soup = multiple_headers_soup
	all_headers = _parse_all_column_headers(soup)
	assert len(all_headers) == 1
	headers = all_headers[0]
	assert len(headers) == 32
	assert headers[0].display_name == 'Rk'
	assert headers[0].class_name == 'ranker'
	assert headers[4].display_name is None
	assert headers[4].class_name == 'player'
	assert headers[30].display_name == 'College/Univ'
	assert headers[30].class_name == 'college_id'

def test_parse_all_data():
	soup = one_table_full_text_soup
	all_tables_rows, all_totals = _parse_all_data(soup)
	rows = all_tables_rows[0]
	assert len(rows) == 5
	assert rows[0][0] == 1
	assert type(rows[0][0]) == int
	assert rows[0][7] == 'HOU'
	assert type(rows[0][7]) == unicode
	assert rows[2][1] == 2014
	assert type(rows[2][1]) == int
	assert rows[2][16] == '3-10-0'
	assert type(rows[2][16]) == unicode
	assert len(all_totals) == 1
	assert all_totals[0] is None

	soup = complicated_soup
	all_tables_rows, all_totals = _parse_all_data(soup)
	assert len(all_tables_rows) == 9
	assert len(all_tables_rows[5]) == 13
	assert len(all_tables_rows[7]) == 27
	assert all_tables_rows[0][0][0] == 'First'
	assert all_tables_rows[8][1][7] == 'SEA 45'
	assert type(all_tables_rows[8][0][3]) == int
	assert type(all_tables_rows[8][0][8]) == unicode
	assert all_tables_rows[8][-1][4] == '11:49'

	assert len([x for x in all_totals if x is not None]) == 7
	assert all_totals[2][0] == 'Pct'
	assert all_totals[0] is None

	soup = multiple_headers_soup
	all_tables_rows, all_totals = _parse_all_data(soup)
	assert all_totals == [None]
	assert len(all_tables_rows) == 1
	assert len(all_tables_rows[0]) == 256
	assert all_tables_rows[0][254][4] == 'Tyler Starr'
	assert type(all_tables_rows[0][254][0]) == int
	

def test_parse_text():

	# Test out one table, full text, not many results
	tables = parse_text(one_table_full_text)

	assert len(tables) == 1
	assert 'Search Form' not in [x.title for x in tables]

	test_table = tables[0]
	assert test_table.title == 'Drafted Players'
	assert len(test_table.headers) == 32
	assert test_table.valid() is True
	assert len(test_table) == 5

	# Testing out muliple headers
	tables = parse_text(multiple_headers)
	assert len(tables) == 1
	assert tables[0].title == 'Drafted Players'

	test_table = tables[0]
	assert len(test_table.headers) == 32
	assert test_table.valid() is True
	assert len(test_table) == 256
	assert test_table[254][4] == 'Tyler Starr'
	assert test_table[0][4] == 'Jadeveon Clowney'
	
	# Test out multiple tables real fast
	tables = parse_text(complicated)
	assert len(tables) == 9
	for table in tables:
		assert table.valid() is True
	length_spec = [3, 4, 2, 2, 2, 13, 8, 27, 125]
	for index, dummy in enumerate(length_spec):
		assert len(tables[index]) == length_spec[index]
