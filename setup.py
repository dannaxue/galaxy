#!/usr/bin/env python
"""Setup script for installing sofia."""

from setuptools import setup 

config = {
    'name': 'galaxy',
    'version': '0.0.1',
    'description': 'GUI',
    'author': 'Danna Xue',
    'author email': 'dannaxue@stanford.edu',
    'url': 'https://github.com/dannaxue/galaxy.git',
    'download_url': 'https://github.com/dannaxue/galaxy',
    'license': 'MIT',
    'packages': ['galaxy'],
    'scripts': ['bin/galaxy'],
    'include_package_data': True,
    'package_data': {'sofia': ['icons/*.png', 'icons/*.gif', 'stylesheet.css']}
}

setup(**config)
