#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import setuptools
import os

versions = list(filter(lambda x: x != "", os.popen(
    "git tag -l").read().split("\n")))
version = versions[-1] if len(versions) > 0 else "UNTAGED-%s" % os.popen(
    "git log --pretty=format:'%H'").read().split("\n")[0]

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")

opts = {
    'name': 'documentDownloader',
    'version': version,
    'author': 'OhYee',
    'author_email': 'oyohyee@oyohyee.com',
    'url': 'https://github.com/OhYee/documentDownloader',
    'description': u'book118文档下载器',
    'long_description': long_description,
    'long_description_content_type': "text/markdown",
    'packages': setuptools.find_packages(),
    'install_requires': requirements,
    'entry_points': {
        'console_scripts': [
            'documentDownloader=book118:main',
        ]
    },
    'classifiers': [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
}

setup(**opts)
