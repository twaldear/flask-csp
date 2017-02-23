from flask import make_response
from functools import wraps
import os
import json

class csp_default:
	default_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'csp_default.json')
	
	def read(self):
		""" read default csp settings from json file """
		with open(self.default_file) as json_file:
			try:
				return json.load(json_file)
			except Exception as e:
				raise 'empty file'
			
	def update(self,updates={}):
		""" 
			update csp_default.json with dict
			
			if file empty add default-src and create dict
		"""
		try:
			csp = self.read()
		except:
			csp = {'default-src':"'self'"}
			self.write(csp)
		csp.update(updates)
		self.write(csp)
		
	def write(self,content):
		fh = open(self.default_file, "w")
		fh.write(json.dumps(content))
		fh.close()

def create_csp_header(cspDict):
	""" create csp header string """
	policy = ['%s %s' % (k, v) for k, v in cspDict.items() if v != '']
	return '; '.join(policy)

def csp_header(csp={}):
    """ Decorator to include csp header on app.route wrapper """
    _csp = csp_default().read()
    _csp.update(csp)
    
    _header = ''
    if 'report-only' in _csp and _csp['report-only'] is True:
    	_header = 'Content-Security-Policy-Report-Only'
    else:
    	_header = 'Content-Security-Policy'
    if 'report-only' in _csp:
    	del _csp['report-only']
    _headers = {_header: create_csp_header(_csp)}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in _headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator
