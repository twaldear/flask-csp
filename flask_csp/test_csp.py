import unittest
import tempfile
from flask import Flask
from flask_csp.csp import csp_default, create_csp_header, csp_header

class CspTestFunctions(unittest.TestCase):
	""" test base functions """
	def setUp(self):
		tmp = tempfile.mkstemp()
		self.dh = csp_default()
		self.dh.default_file = tmp[1]

	def test_create_csp_header(self):
		""" test dict -> csp header """
		self.assertEquals(create_csp_header({'foo':'bar','lorem':'ipsum'}),'foo bar; lorem ipsum')
	
	def test_default_empty_exception(self):
		""" test empty default file """
		with self.assertRaises(Exception):
			self.dh.read()
	
	def test_default_read_write(self):
		""" test read/write to default """
		self.dh.update() # test empty file
		t = self.dh.read()
		self.assertEquals(t['default-src'],"'self'")
		
		self.dh.update({'default-src':"'none'",'script-src':"'self'"}) # test update
		t = self.dh.read()
		self.assertEquals(t['default-src'],"'none'")
		self.assertEquals(t['script-src'],"'self'")
		
	def test_included_json_file(self):
		""" make sure included json file is readable / writeable """
		h = csp_default()
		ret = h.read()
		assert "default-src" in ret
		
		h.update({'default-src':"'self'"})
		ret = h.read()
		self.assertEquals(ret['default-src'],"'self'")		

class CspTestDefaultDecorator(unittest.TestCase):
	""" test decorator with no values passed """
	def setUp(self):
		self.app = Flask(__name__)
		@self.app.route('/')
		@csp_header()
		def index():
			return "test"

	def test_csp_header(self):
		with self.app.test_client() as c:
			result = c.get('/')
			assert "default-src 'self'" in result.headers.get('Content-Security-Policy')

class CspTestCustomDecoratorUpdate(unittest.TestCase):
	""" test decorator with custom values passed by dict """
	def setUp(self):
		self.app = Flask(__name__)
		@self.app.route('/')
		@csp_header({'default-src':"'none'",'script-src':"'self'"})
		def index():
			return "test"

	def test_csp_header(self):
		with self.app.test_client() as c:
			result = c.get('/')
			assert "default-src 'none'" in result.headers.get('Content-Security-Policy')
			assert "script-src 'self'" in result.headers.get('Content-Security-Policy')

class CspTestCustomDecoratorRemove(unittest.TestCase):
	""" test removing policy through custom decorator values """
	def setUp(self):
		self.app = Flask(__name__)
		@self.app.route('/')
		@csp_header({'default-src':''})
		def index():
			return "hi"

	def test_csp_header(self):
		with self.app.test_client() as c:
			result = c.get('/')
			assert "default-src" not in result.headers.get('Content-Security-Policy')

class CspTestReadOnly(unittest.TestCase):
	""" test read only """
	def setUp(self):
		self.app = Flask(__name__)
		@self.app.route('/')
		@csp_header({'report-only':True})
		def index():
			return "hi"

	def test_csp_header(self):
		with self.app.test_client() as c:
			result = c.get('/')
			assert "default-src" in result.headers.get('Content-Security-Policy-Report-Only')
			assert "report-only" not in result.headers.get('Content-Security-Policy-Report-Only')

if __name__ == '__main__':
    unittest.main()
