#!/usr/bin/env python

import configparser
import re

from setuptools import setup, find_packages


def long_description():
    with open('README.md') as fd:
        return fd.read()


def _get_pyproject_cfg():
    parser = configparser.ConfigParser()
    with open('pyproject.toml') as fd:
        parser.read_file(fd)
    return parser


def _extract_version(text):
    try:
        return re.findall(r'[\w\.]+', text)[0]
    except IndexError:
        return ''


def version():
    return _get_pyproject_cfg()['tool.poetry']['version'].strip('"')


def install_requires():
    cfg = _get_pyproject_cfg()
    deps = cfg['tool.poetry.dependencies']
    seq = (
        (k, _extract_version(v)) for k, v in deps.items() if k != 'python'
    )
    return [f'{k}=={v}' for k, v in seq]


setup(
    name='simple-mailer',
    version=version(),
    author='Rigel Di Scala',
    author_email='zedr@zedr.com',
    description='A simple mailer for web forms',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/zedr/simple-mailer',
    install_requires=install_requires(),
    package_dir={'': 'src'},
    packages=['simple_mailer'],
    py_modules=['simple_mailer.web'],
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
