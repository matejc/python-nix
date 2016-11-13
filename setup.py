#!/usr/bin/env python3

import os

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_swagger',
    'webcolors',
    'rfc3987',
    'strict-rfc3339',
    'pyramid_tm',
    'pyramid_zodbconn',
    'transaction',
    'ZODB3',
    'waitress',
]

# tests_require = [
#     'WebTest >= 1.3.1',  # py3 compat
#     'pytest',  # includes virtualenv
#     'pytest-cov',
# ]

setup(
    name='python-nix',
    version='0.0',
    description='python-nix',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='pyramid nix api',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # extras_require={
    #     'testing': tests_require,
    # },
    install_requires=requires,
    entry_points="""\
      [paste.app_factory]
      main = nix.api:main
      """, )
