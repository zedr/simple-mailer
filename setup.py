#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='simple-mailer',
    version='1.0',
    author='Rigel Di Scala',
    author_email='zedr@zedr.com',
    install_requires=['bottle'],
    package_dir={'': 'src'},
    packages=find_packages(),
    entry_points={
        "console_scripts": ["simple-mailer=simple_mailer.web:run_application"]
    }
)
