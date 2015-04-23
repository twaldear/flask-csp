from setuptools import setup

import flask_csp

setup(
  name = 'flask-csp',
  py_modules = ['flask_csp'],
  packages = ['flask_csp'],
  include_package_data = True,
  package_data = {'':['csp_default.json']},
  version = '0.37',
  description = 'Flask Content Security Policy header support',
  long_description = """
Add a Content Security Policy header to your Flask application. 

Mitigate the risk of cross-site scripting attacks by whitelisting trusted origins with a Content Security Policy. 
"""
  license='MIT',
  author = 'Tristan Waldear',
  author_email = 'trwaldear@gmail.com',
  url = 'https://github.com/twaldear/flask-csp',
  download_url = 'https://github.com/twaldear/flask-csp/tarball/0.1',
  keywords = ['flask', 'csp', 'header'],
  classifiers=[
    'Programming Language :: Python :: 2',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ]
)