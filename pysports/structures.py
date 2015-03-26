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

	name = None
	"Printed name for the header"

	description = None
	"Printed description on the header, when you tooltip over it"

	def __init__(self, name = None, description = None):
		self.name = name
		self.description = description

	def __str__(self):
		return "ColumnHeader name: '%s', description: '%s'" % (self.name, self.description)
