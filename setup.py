#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='simple-mailer',
    version='0.9.0',
    author='Rigel Di Scala',
    author_email='zedr@zedr.com',
    description='A simple mailer for web forms',
    url='https://github.com/zedr/simple-mailer',
    install_requires=['bottle', 'lxml', 'jinja2'],
    package_dir={'': 'src'},
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['simple-mailer=simple_mailer.web:run_application']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7'
)
