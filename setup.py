from setuptools import setup

setup(
  name = 'flask-csp',
  packages = ['flask-csp'],
  version = '0.1',
  description = 'Flask Content Security Policy header support',
  license='MIT',
  author = 'Tristan Waldear',
  author_email = 'trwaldear@gmail.com',
  url = 'https://github.com/twaldear/flask-csp',
  download_url = 'https://github.com/twaldear/flask-csp/tarball/0.1',
  install_requires=[
        'Flask'
  ],
  classifiers = [],
)