#!/usr/bin/env python

from setuptools import setup


def long_description():
    with open('README.md') as fd:
        return fd.read()


setup(
    name='simple-mailer',
    version='0.15.3',
    author='Rigel Di Scala',
    author_email='zedr@zedr.com',
    description='A simple mailer for web forms',
    license='MIT',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/zedr/simple-mailer',
    install_requires=[
        'bottle==0.12.18',
        'lxml==4.5.0',
        'jinja2==2.11.2'
    ],
    package_dir={'': 'src'},
    packages=['simple_mailer'],
    py_modules=['simple_mailer'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['simple-mailer=simple_mailer.web:main']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7'
)
