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
<<<<<<< HEAD
    #packages = ['beautifulsoup', 'bs4', 'requests'],
    download_url = 'https://github.com/AndersFluur/Norwegian/tarball/0.1', 
=======
    download_url = 'https://github.com/AndersFluur/Norwegian/tarball/1.0', 
>>>>>>> Made working python package with license entry-points, etc
    keywords = ['airlines', 'travel'],
    classifiers = [],

    entry_points = {
                    'console_scripts': ['norwegian=norwegian.norwegian:main'],
    },

    install_requires=[
           'bs4',
<<<<<<< HEAD
#           'beautifulsoap4',
=======
>>>>>>> Made working python package with license entry-points, etc
           'requests'
    ],

)
