__doc__ = """
All structures for holding table data
"""

try:
	import ast
except ImportError:
	import sys
	sys.stderr.write('Unable to import the ast module: do you have a Python version 2.6 or newer?\n')
	sys.exit(1)

class Table(list):
	"""Main object holding a statistics table parsed from the HTML.  Iterator returns the rows, top to bottom."""

	title = None
	"Title of the dataset, for identification"

	headers = None
	"Last-level headers on each of the columns, right before the data"

	def __init__(self):
		self.title = None
		self.headers = []

	def valid(self):
		"Defines if we currently believe this is a 'valid' table in the construction process.  True if it is, False if it isn't"
		for row in self:
			if len(row) != len(self.headers):
				return False

		return True

	def __repr__(self):
		return list.__repr__(self)

# Functionality we could add to a Row:
#  - Save the data row label for re-sorting purposes later
class Row(list):
	"""Row for a data table.  Iterator returns Cell objects, left to right"""

	def __repr__(self):
		return list.__repr__(self)

	def sieve(self, data):
		"""Insert an item, determining its data type"""
		try:
			new_item = ast.literal_eval(data)
		except StandardError as e:
			new_item = data

		self.append(new_item)

# Functionality that we could add to a Cell:
#  - Try to de-multiplex some of the links if there are any, or store them in an additional variable
class Cell(object):

	contents = None

	def __init__(self, data):
		"""Try to determine the type of data we got and make a cell out of it.  Will default to 'string' if something goes wrong."""


class ColumnHeader(object):
	"""Last-level column header before the data"""

	display_name = None
	"Printed name for the header"

	class_name = None
	"Sorting descriptor for the header; a little more meaningful"

	def __init__(self, display_name = None, class_name = None):
		self.display_name = display_name
		self.class_name = class_name

	def __repr__(self):
		return self.__str__() + '\n'

	def __str__(self):
		return "ColumnHeader Instance\n\tshort: '%s'\n\tlong: '%s'" % (self.display_name, self.class_name)
