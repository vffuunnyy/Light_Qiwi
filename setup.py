# -*- coding: utf-8 -*-
from setuptools import setup

"""
:authors: vffuunnyy
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2019 vffuunnyy
"""

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Light_Qiwi',
    version='1.0.1',
    packages=['Light_Qiwi'],
    url='https://github.com/vffuunnyy/Light_Qiwi',
    license='Apache License, Version 2.0, see LICENSE file',
    author='vffuunnyy',
    author_email='vffuunnyy@gmail.com',
    setup_requires=['pyversion'],
    auto_version=True,
    description='Python модуль для написания скриптов для Qiwi (qiwi.com) (API wrapper)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'cherrypy', 'aenum'],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
