#!/usr/bin/env python

from setuptools import setup

setup(
    name='norwegian',
    packages = ['norwegian'],
    version = '1.0',
    description = 'Read and present flights from the Norwegian web site',
    author = 'Anders Fluur',
    author_email = 'anders@fluurnet',
    url = 'https://github.com/AndersFluur/Norwegian',
    #packages = ['beautifulsoup', 'bs4', 'requests'],
    download_url = 'https://github.com/AndersFluur/Norwegian/tarball/0.1', 
    keywords = ['airlines', 'travel'],
    classifiers = [],

    entry_points = {
                    'console_scripts': ['norwegian=norwegian.norwegian:main'],
    },

    install_requires=[
           'bs4',
#           'beautifulsoap4',
           'requests'
    ],

)
