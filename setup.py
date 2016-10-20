#!/usr/bin/env python

from setuptools import setup

setup(
    name='norwegian',
    packages = ['norwegian'],
    version = '1.0.1',
    description = 'Read and present flights from the Norwegian web site',
    author = 'Anders Fluur',
    author_email = 'anders@fluurnet',
    url = 'https://github.com/AndersFluur/Norwegian',
    download_url = 'https://github.com/AndersFluur/Norwegian/tarball/1.0.1', 
    keywords = ['airlines', 'travel'],
    classifiers = [],

    entry_points = {
                    'console_scripts': ['norwegian=norwegian.norwegian:main'],
    },

    install_requires=[
           'bs4',
           'requests'
    ],

)
