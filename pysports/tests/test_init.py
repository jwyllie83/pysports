import os
from pysports import parse_text

cwd = os.path.dirname(os.path.realpath(__file__))

def test_parse_text():
	with open(cwd + '/drafts_small.html') as handle:
		text = handle.read()

	parse_text(text)
