import os
from pysports import parse_text

cwd = os.path.dirname(os.path.realpath(__file__))

one_table_full_text = None

def setup():
	global one_table_full_text
	with open(cwd + '/drafts_small.html') as handle:
		one_table_full_text = handle.read()

def test_parse_text():

	# Test out one table, full text, not many results
	tables = parse_text(one_table_full_text)

	assert len(tables) == 1
	assert tables[0].title == 'Drafted Players'
	assert 'Search Form' not in [x.title for x in tables]
	test_table = tables[0]
#	assert len(test_table) == 5
