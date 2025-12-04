# -*- coding: utf-8 -*-
#
# This file is part of Flask-Gravatar
# Copyright (C) 2015, 2017 CERN.
#
# Flask-Gravatar is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Small extension for Flask to make usage of Gravatar service easy."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    # 'pytest-pep8>=1.0.6', # Removed deprecated plugin
    'pytest>=2.8.0',
    'flake8', # Added to ensure comprehensive PEP 8 style checking
]


extras_require = {
    'docs': [
        'Sphinx>=1.4.2',
        'pygments', # Added to fix ModuleNotFoundError when building docs
        ],
        'tests': tests_require,
        }

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    # 'pytest-runner>=2.6.2', # Removed deprecated dependency
]

install_requires = [
    'Flask>=0.10',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('flask_gravatar', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='Flask-Gravatar',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='flask gravatar',
    license='BSD',
    author='Alexander Zelenyak aka ZZZ',
    author_email='zzz.sochi@gmail.com',
    url='https://github.com/zzzsochi/Flask-Gravatar/',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    # REMOVED DEPRECATED ARGUMENTS (tests_require and setup_requires)
    # setup_requires=setup_requires,
    # tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # Dropped EOL Python Versions (2.x, 3.4-3.7)
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8', # New minimum supported version
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13', 
        'Programming Language :: Python :: 3.14',
        'Development Status :: 5 - Production/Stable',
    ],
)
