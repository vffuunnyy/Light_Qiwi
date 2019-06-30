# -*- coding: utf-8 -*-
from setuptools import setup

"""
:authors: vffuunnyy
:license: Apache License, Version 2.0
:copyright: (c) 2019 vffuunnyy
"""

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='Light_Qiwi',
    version='0.1',
    packages=['Light_Qiwi'],
    url='https://github.com/vffuunnyy/Light_Qiwi',
    license='Apache License, Version 2.0',
    author='vffuunnyy',
    author_email='vffuunnyy@gmail.com',
    setup_requires=['pyversion'],
    auto_version=True,
    description=u'Python модуль для написания скриптов для Qiwi (qiwi.com) (API wrapper)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'cherrypy', 'aenum'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
