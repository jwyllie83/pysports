__doc__ = """
All structures for holding table data
"""

class Table(list):
	"""Main object holding a statistics table parsed from the HTML.  Iterator returns the rows"""

	title = None
	"Title of the dataset, for identification"

	headers = None
	"Last-level headers on each of the columns, right before the data"

	def __init__(self):
		self.title = None
		self.headers = []

	def valid(self):
		"Defines if we currently believe this is a 'valid' table in the construction process.  True if it is, False if it isn't"
		if len(self) != len(self.headers):
			return False

		return True

class Row(object):
	pass

class Item(object):
	pass

class ColumnHeader(object):
	"""Last-level column header before the data"""

	display_name = None
	"Printed name for the header"

	class_name = None
	"Sorting descriptor for the header; a little more meaningful"

	def __init__(self, display_name = None, class_name = None):
		self.display_name = display_name
		self.class_name = class_name

	def __str__(self):
		return "ColumnHeader Instance\n\tshort: '%s'\n\tlong: '%s'" % (self.display_name, self.class_name)
