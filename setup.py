# -*- coding: utf-8 -*-
from setuptools import setup

"""
:authors: vffuunnyy
:license: Apache License, Version 2.0
:copyright: (c) 2020 vffuunnyy
"""

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='light_qiwi',
    version='1.3.1',
    packages=['light_qiwi'],
    url='https://github.com/vffuunnyy/Light_Qiwi',
    license='Apache License, Version 2.0',
    author='vffuunnyy',
    author_email='vffuunnyy@gmail.com',
    setup_requires=['pyversion'],
    auto_version=True,
    description=u'Python модуль для обработки платежей Qiwi (qiwi.com) (API wrapper)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'aenum'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
