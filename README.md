# flask-csp

Add a Content Security Policy header to your Flask application.
More information on CSP:
* [w3c documentation](http://www.w3.org/TR/CSP2/)
* [useful guide](http://www.html5rocks.com/en/tutorials/security/content-security-policy/)

## Installation
Install the extension with using pip, or easy_install. [Pypi Link](https://pypi.python.org/pypi/flask-csp)
```bash
$ pip install flask-csp
```

## Usage
Add the csp_header(...) decorator after the app.route(...) decorator to create a csp header on each route. The decorator can either be passed no value (Add default policies) or custom values by a dict (Add custom policies). For more information on the default policies see "Change Default Policies" below.

### Add default header
```python
from flask_csp.csp import csp_header
...
@app.route('/')
@csp_header()
```
### Add custom header
Pass the csp_header wrapper a dict with the policies to change:
```python
from flask_csp.csp import csp_header
...
@app.route('/')
@csp_header({'default-src':"'none'",'script-src':"'self'"})
```
Notes: 
* Only policies with a non empty value are added to the header. The wrapper @csp_header({'default-src':""}) will remove 'default-src ...' from the header
* 4 keywords in policies must always be encapsulated in single quotes: 'none', 'self', 'unsafe-inline','unsafe-eval'

### Report only header
To set the header to "Report only" pass the key/value pair 'report-only':True to the custom header dict:
```python
from flask_csp.csp import csp_header
...
@app.route('/')
@csp_header({'report-only':True})
```

## Change Default Policies
The default policies are as follows:
```json
{
  "default-src": "'self'",
  "script-src": "",
  "img-src": "",
  "object-src": "",
  "plugin-src": "",
  "style-src": "",
  "media-src": "",
  "child-src": "",
  "connect-src": "",
  "base-uri": "",
  "report-uri": "/csp_report"
}
```
Editing of the default policies can be done via command line:
```python
>>> from flask_csp.csp import csp_default
>>> h = csp_default()
>>> h.update({'child-src':"'self'"})
```

To view the default policies:
```python
>>> from flask_csp.csp import csp_default
>>> h = csp_default()
>>> h.read()
```
Note: 
* Python interpreter must be reloaded for changes to the default policies to take place

## Violation Reports
Based on the default settings, reports will be sent to the route 'csp_report' through a POST request. This is totally customizable but here is a very simplistic example of handling these reports:
```python
@app.route('/csp_report',methods=['POST'])
def csp_report():
	with open('/var/log/csp/csp_reports'), "a") as fh:
		fh.write(request.data+"\n")
	return 'done'
```
