#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup

import getctstream
from os.path import *

setup(name='getctstream',
        version = getctstream.__version__,
        description = 'Python script pro získání streamů živého vysíláni programů České Televize',
        long_description = open(join(dirname(__file__), 'README.md')).read(),
        author = 'Jiří Kuneš',
        author_email = 'jirka642@gmail.com',
        url = 'https://github.com/kunesj/GetCTStream',
        packages = ['getctstream'],
        include_package_data = True,
        license = "GPL3",
        entry_points = {
        'console_scripts': ['getctstream = getctstream.cli_interface:main']
        },
        install_requires = [
          'setuptools',
          'requests'
        ],
    )
