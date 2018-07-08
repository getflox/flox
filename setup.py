#!/usr/bin/env python
import json
from os.path import dirname, abspath

from setuptools import setup, find_packages


with open('Pipfile.lock') as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['default'].items()
    ]
    tests_require = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['develop'].items()
    ]

setup(
    name='flox',
    version='0.1',
    description='Consistent project management',
    packages=find_packages(where=dirname(abspath(__file__))),
    entry_points={
        'console_scripts': [
            'flox=flox.cli:cli'
        ]
    },
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires='>=3.6'
)
