#!/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# README is required for distribution, but README.md is required for github,
#   so create README temporarily
README_SRC = os.path.join(ROOT_DIR, 'README.md')
os.system('cp %s %s' % (README_SRC, os.path.join(ROOT_DIR, 'README.txt')))

with open(README_SRC, 'r') as f:
    readme_text = f.read()

sdict = dict(
    name = 'django-html5-boilerplate',
    packages = find_packages(),
    version='.'.join(map(str, __import__('dh5bp').__version__)),
    description = 'A framework that includes the HTML5 boilerplate template into your django project.',
    long_description=readme_text,
    url = 'https://github.com/mattsnider/django-html5-boilerplate',
    author = 'Matt Snider',
    author_email = 'admin@mattsnider.com',
    maintainer = 'Matt Snider',
    maintainer_email = 'admin@mattsnider.com',
    keywords = ['python', 'django'],
    license = 'MIT',
    include_package_data=True,
    install_requires=[
        'django>=1.3',
#        'fabric>=1.7.0', # required to build, but not to use
    ],
    platforms=["any"],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

from distutils.core import setup
setup(**sdict)

# cleanup README
os.remove('%s/README.txt' % ROOT_DIR)